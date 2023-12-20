from mousetumornet import predict, postprocess
import tifffile
from pathlib import Path
import argparse
import glob

from mousetumornet.configuration import MODELS
from mousetumornet.roi import compute_roi

def process_input_file_predict(input_image_file, model):
    image = tifffile.imread(input_image_file)

    # (TODO) Assert some stuff about the image
    # ...

    pred = predict(image, model=model)
    post = postprocess(pred)

    pt = Path(input_image_file)
    out_file_name = pt.parent / f'{pt.stem}_mask.tif'

    tifffile.imwrite(out_file_name, post)
    print('Wrote to ', out_file_name)


def cli_predict_image():
    """Command-line entry point for model inference."""
    parser = argparse.ArgumentParser(description='Use this command to run inference.')
    parser.add_argument('-i', type=str, required=True, help='Input image. Must be either a TIF or a NIFTI image file.')
    parser.add_argument('-m', type=str, required=True, help='Model name. Check the doc for available models.')
    args = parser.parse_args()

    # image_stem, image_ext = os.path.splitext(input_image_file)
    input_image_file = args.i
    model = args.m

    assert model in MODELS.keys(), f'Your model {model} is not available. Choose from: {list(MODELS.keys())}'

    process_input_file_predict(input_image_file, model)


def cli_predict_folder():
    parser = argparse.ArgumentParser(description='Use this command to run inference in batch on a given folder.')
    parser.add_argument('-i', type=str, required=True, help='Input folder. Must contain suitable TIF image files.')
    parser.add_argument('-m', type=str, required=True, help='Model name. Check the doc for available models.')
    args = parser.parse_args()

    input_folder = args.i
    model = args.m

    assert model in MODELS.keys(), f'Your model {model} is not available. Choose from: {list(MODELS.keys())}'

    for input_image_file in glob.glob(str(Path(input_folder) / '*.tif')):
        process_input_file_predict(input_image_file, model)


def process_input_file_extract_roi(input_image_file):

    image = tifffile.imread(input_image_file)

    *_, roi = compute_roi(img=image)

    pt = Path(input_image_file)
    out_file_name = pt.parent / f'{pt.stem}_roi.tif'

    tifffile.imwrite(out_file_name, roi)
    print('Wrote to ', out_file_name)


def cli_extract_roi():
    """Command-line entry point for roi extraction."""
    parser = argparse.ArgumentParser(description='Use this command to run inference.')
    parser.add_argument('-i', type=str, required=True, help='Input image. Must be a TIF file.')
    args = parser.parse_args()

    input_image_file = args.i

    process_input_file_extract_roi(input_image_file)

    
