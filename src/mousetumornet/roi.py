import numpy as np
import pandas as pd
from scipy.ndimage import binary_fill_holes, label
from skimage.filters import threshold_otsu
from skimage.measure import regionprops_table
from skimage.segmentation import chan_vese, morphological_chan_vese


def normalize_image(img):
    if (img.min() == 0.0) & (img.max() == 1.0):
        img_normed = img.astype(np.float32)
    else:
        image = img.astype(np.float32)
        mi = np.percentile(image, 2)
        ma = np.percentile(image, 98)
        img_normed = (image - mi) / ( ma - mi + 1e-20 )
    
    return img_normed


def segment_body(image: np.ndarray) -> np.ndarray:
    """Segments the body of the mouse using Chan-Vese morphological acive contours"""
    # Ignore first Z slices which are all zeros
    for i, frame in enumerate(image):
        if frame.sum():
            break
    # Same for last slices
    for j, frame in enumerate(image[::-1]):
        if frame.sum():
            break

    end_z = image.shape[0] - j

    labels = np.zeros_like(image, dtype=np.uint8)
    labels[i] = binary_fill_holes(
        chan_vese(image[i], init_level_set="checkerboard", tol=1e-5)
    )
    for k, frame in enumerate(image[i + 1 : end_z]):
        labels[k + i + 1] = morphological_chan_vese(
            image[k + i], init_level_set=labels[k + i], num_iter=5
        )

    labels = keep_biggest_object(labels)

    return labels


def keep_biggest_object(lab_int: np.ndarray) -> np.ndarray:
    """Selects only the biggest object of a labels image."""
    labels = label(lab_int)[0]  # label from scipy
    counts = np.unique(labels, return_counts=1)
    biggestLabel = np.argmax(counts[1][1:]) + 1
    return (labels == biggestLabel).astype(int)


def get_lungs_bbox(image: np.ndarray, body_mask: np.ndarray) -> np.ndarray:
    lungs_pre_mask = (image < threshold_otsu(image)).astype(np.uint8)
    lungs_pre_mask[body_mask == 0] = 0  # Remove the outside region
    lungs_pre_mask = keep_biggest_object(lungs_pre_mask)

    props = regionprops_table(lungs_pre_mask, properties=["bbox"])
    x0 = int(props["bbox-0"])
    x1 = int(props["bbox-3"])
    y0 = int(props["bbox-1"])
    y1 = int(props["bbox-4"])
    z0 = int(props["bbox-2"])
    z1 = int(props["bbox-5"])
    lungs_bbox = image[x0:x1, y0:y1, z0:z1].copy()

    return props, lungs_bbox


def compute_roi(img: np.ndarray):
    """Computes and saves a ROI for a given image."""
    img_normed = normalize_image(img)

    body = segment_body(img_normed)

    props, lungs_bbox_data = get_lungs_bbox(img_normed, body)

    df = pd.DataFrame(props)

    x0 = int(df["bbox-0"])
    x1 = int(df["bbox-3"])
    y0 = int(df["bbox-1"])
    y1 = int(df["bbox-4"])
    z0 = int(df["bbox-2"])
    z1 = int(df["bbox-5"])

    roi = img[x0:x1, y0:y1, z0:z1]

    return df, lungs_bbox_data, body, roi


def compute_roi_bones(img: np.ndarray, q=0.99):
    """Computes a ROI encompassing the bones in the image - based on quantiles."""
    bones = (img > np.quantile(img, q)).astype(np.uint8)
    if bones.sum() == 0:
        print("It looks like no bones were segmented.")
        x0 = 0
        y0 = 0
        z0 = 0
        x1, y1, z1 = img.shape
    else:
        props = regionprops_table(bones, properties=["bbox"])
        
        df = pd.DataFrame(props)

        x0 = int(df["bbox-0"].values[0])
        x1 = int(df["bbox-3"].values[0])
        y0 = int(df["bbox-1"].values[0])
        y1 = int(df["bbox-4"].values[0])
        z0 = int(df["bbox-2"].values[0])
        z1 = int(df["bbox-5"].values[0])

    roi = img[x0:x1, y0:y1, z0:z1]

    return df, roi, bones, roi