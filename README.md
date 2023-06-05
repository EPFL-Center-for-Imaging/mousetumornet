# 🫁 Lung tumor nodules segmentation in mice CT scans

[![License BSD-3](https://img.shields.io/pypi/l/napari-label-focus.svg?color=green)](https://github.com/MalloryWittwer/napari-label-focus/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-label-focus.svg?color=green)](https://pypi.org/project/napari-label-focus)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-label-focus)](https://napari-hub.org/plugins/napari-label-focus)

We provide a neural network model for lung tumor nodule segmentation in mice. The model is based on the [nnUNet](https://github.com/MIC-DKFZ/nnUNet) framework which we used in the full resolution 3D configuration (3d_fullres).

<!-- <div style="text-align:center"><img src="images/main_fig.png" height="400"></div> -->
<p align="center">
    <img src="images/main_fig.png" height="400">
</p>

The goal of our tool is to facilitate the annotation of individual lung tumor nodules in mouse CT scans. The U-net model produces a binary mask representing the foreground tumor class. The tumor nodules are individually labeled based on the connected components method.

## Try the model on your data

- [Check the input data specifications](#input-data)
- [Check the hardware requirements](#hardware-requirements)
- [Install the package](#installation)
- [Follow the usage instructions](#usage-in-napari)

## Input data specifications

Make sure that your input data is compatible with our model. To check the integrity of your input data, read [Input data requirements](documentation/data_specs.md).

**Sample data:** (Option 1) A few example images from our training dataset are available for download on [Zenodo](https://sandbox.zenodo.org/record/1205983/files/1493.tif). *(Option 2) The full training set. [??]*

## Hardware requirements

Installing PyTorch with CUDA support and using a GPU for inference is strongly recommended. We report the following runtimes for inference on a GPU and CPU, respectively:

- GPU (RTX 3060, 12 GB RAM): **12 sec**.
- CPU (AMD Ryzen 9 5900X (Zen 3, 64MB L3), 12 Threads): **68 sec**.

## Installation

We recommend performing the installation in a clean Python environment. If you are new to Python, read our [beginner's guide](documentation/beginner_guide.md) to learn how to do that.

The code requires `python>=3.9`, as well as `pytorch>=2.0`. If wish to use a GPU with CUDA support, you may want to install Pytorch first and separately following the instructions for your platform on [pytorch.org](https://pytorch.org/get-started/locally/).

Install `mousetumornet` from the repository:

```
pip install git+https://gitlab.epfl.ch/center-for-imaging/mousetumornet.git
```

or clone the repository and install with:

```
git clone git+https://gitlab.epfl.ch/center-for-imaging/mousetumornet.git
cd mousetumornet
pip install -e .
```

## Models

The model weights (~461 MB) are automatically downloaded from Zenodo the first time you run inference. The model files are saved in the user home folder in the `.nnunet` directory.

New versions of the model, trained on more annotated data, faster, or more performant, are to be released in the future. As of June 2023, the available models are:

- [Model-v1.0]() | Accuracy | Training images | Name (v1)
- [Model-v2.0]() | Accuracy | Training images | Name (v2)

These models are all available for use in our package and can be selected by the user (see [Usage](#usage-in-napari)).


## Usage in Napari

[Napari](https://napari.org/stable/) is a multi-dimensional image viewer for python. To use our model in Napari, start the viewer with

```
napari
```

To open an image, use `File > Open files` or drag-and-drop an image into the viewer window. If you want to open medical image formats such as NIFTI directly, consider installing the [napari-medical-image-formats](https://pypi.org/project/napari-medical-image-formats/) plugin.

**Sample data**: To test the model, you can run it on our provided sample image. In Napari, open the image from `File > Open Sample > Mouse lung CT scan`.

Next, in the menu bar select `Plugins > mousetumornet > Tumor detection`. Select a [model](#models) and run it on your selected image by pressing the "Detect tumors" button.

<p align="center">
    <img src="images/napari-screenshot.png" height="400">
</p>

To inspect the results, you can bring in a table representing the detected objects from `Plugins > napari-label-focus > Data table`. Clicking on the data table rows will focus the viewer on the selected object.

## Usage as a library

You can run a model (`v1` in the example below) in just a few lines of code to produce a segmentation mask from an image (represented as a numpy array).

```
from mousetumornet import predict, postprocess

binary_mask = predict(your_image, model='v1')
instances_mask = postprocess(binary_mask)
```

## Usage as a CLI

Run inference on an image from the command-line. For example:

```
mtn_predict_image -i /path/to/folder/image_001.tif/ -m <model_name>
```

The `<model_name>` should be in the [model list](#models), for example `v1`.

The command will save a mask next to the image:
```
folder/
    ├── image_001.tif
    ├── image_001_mask.tif
```

Run inference in batch on all images in a folder:

```
mtn_predict_folder -i /path/to/folder/ -m <model_name>
```
Will produce:
```
folder/
    ├── image_001.tif
    ├── image_001_mask.tif
    ├── image_002.tif
    ├── image_002_mask.tif
```

## Usage recommendation

For use in a scientific context, we believe the model outputs should be considered as an initial guess for the segmentation and not as a definitive result. Certain deviations in the the instrumentation, acquisition parameters, or morphology of the tumor nodules, among other things, can affect performance of the model. Therefore, the detections should always be reviewed by human experts and corrected when necessary.

## Dataset

Our latest model was trained on `493` images from Y separate experiments and validated on 97 images. The data was annotated by Z independent experts from Prof. De Palma's lab in EPFL. The images were acquired over a period of about 12 months using two different CT scanners. In this dataset, we report a dice score performance of 0.63 on the validation images.

The dataset is avaiable for download on [Zenodo](). By downlodading the dataset you agree that you have read and accepted the terms of the [dataset license]().

## Contributing

Contributions are very welcome. Tests can be run with [tox](), please ensure the coverage at least stays the same before you submit a pull request.

## Issues

If you encounter any problems, please file an issue along with a detailed description.

## License

This model is licensed under the [BSD-3](LICENSE.txt) license.

## Carbon footprint of this project

As per the online tool [*Green algorithms*](http://calculator.green-algorithms.org/), the footprint of training the mouse tumor net model was estimated to be 105 g CO2e.

## Citing

Please use the following BibTeX entry to cite this project:

```
article
```