import glob
import os
import shutil
import subprocess
import nibabel as nib
import numpy as np
import pooch
from pooch import Unzip
import scipy.ndimage as ndi
import skimage.morphology

from mousetumornet.configuration import MIN_SIZE_PX

nnUNet_results = os.path.expanduser(
    os.getenv(
        "nnUNet_results", os.path.join(os.getenv("XDG_DATA_HOME", "~"), ".nnunet")
    )
)

os.environ["nnUNet_results"] = nnUNet_results

INPUT_FOLDER = os.path.join(nnUNet_results, "tmp", "nnunet_input")
OUTPUT_FOLDER = os.path.join(nnUNet_results, "tmp", "nnunet_output")

def predict(image: np.ndarray) -> np.ndarray:
    """TODO"""

    pooch.retrieve(
        url="https://sandbox.zenodo.org/record/1204918/files/nnunetv2_weights_fullres.zip",
        known_hash="d26e446d7b95934c958f6a4cb23ced5399c636c599463ebe414d76474588d442",
        path=nnUNet_results,
        progressbar=True,
        processor=Unzip(extract_dir=nnUNet_results)
    )

    if not os.path.exists(INPUT_FOLDER): os.makedirs(INPUT_FOLDER)
    if not os.path.exists(OUTPUT_FOLDER): os.makedirs(OUTPUT_FOLDER)

    nib.save(nib.Nifti1Image(image, None), os.path.join(INPUT_FOLDER, "img_0000.nii.gz"))

    subprocess.run([
        "nnUNetv2_predict", 
        "-i", INPUT_FOLDER, 
        "-o", OUTPUT_FOLDER,
        "-d", "001",
        "-f", "0",
        "-c", "3d_fullres",
        "-device", "cuda",
        # "-device", "cpu",
        "--disable_tta"
    ])

    output_preds_file = list(glob.glob(os.path.join(OUTPUT_FOLDER, "*.gz")))[0]
    image_pred = nib.load(output_preds_file).get_fdata()

    shutil.rmtree(str(INPUT_FOLDER))
    shutil.rmtree(str(OUTPUT_FOLDER))

    return image_pred


def postprocess(segmentation: np.ndarray) -> np.ndarray:
    """Connected components labelling and holes-filling"""
    segmentation = segmentation.astype('uint16')

    ndi.label(segmentation, output=segmentation)
    skimage.morphology.remove_small_objects(segmentation, min_size=MIN_SIZE_PX, out=segmentation)
    ndi.label(segmentation, output=segmentation)

    # Fill holes in each Z slice
    for label_index in range(1, np.max(segmentation)):
        lab_filt = segmentation == label_index
        lab_int = lab_filt.astype(int)
        props = skimage.measure.regionprops_table(lab_int, properties=["bbox"])
        for z in range(int(props["bbox-0"]), int(props["bbox-3"])):
            lab_int[z] = ndi.binary_fill_holes(lab_int[z])
        segmentation[lab_filt] = 0
        segmentation[lab_int > 0] = label_index

    return segmentation



