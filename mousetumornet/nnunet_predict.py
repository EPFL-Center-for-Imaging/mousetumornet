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

from mousetumornet.configuration import MIN_SIZE_PX, MODELS

import torch

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

def predict(image: np.ndarray, model: str) -> np.ndarray:
    """TODO"""

    model_url, model_known_hash = MODELS.get(model)

    nnUNet_results = os.path.expanduser(os.path.join(os.getenv("XDG_DATA_HOME", "~"), ".nnunet", model))

    os.environ["nnUNet_results"] = nnUNet_results

    INPUT_FOLDER = os.path.join(nnUNet_results, "tmp", "nnunet_input")
    OUTPUT_FOLDER = os.path.join(nnUNet_results, "tmp", "nnunet_output")

    pooch.retrieve(
        url = model_url,
        known_hash= model_known_hash,
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
        "-device", DEVICE,
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



