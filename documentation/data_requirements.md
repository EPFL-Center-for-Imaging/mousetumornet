# Input data requirements

## Imaging modality and acquisition

We used two different CT scanners to produce training images. The voxel resolution was [...] and [Other specs].

## Region of interest (ROI)

We tested the model on regions of interest (ROIs) in the lung parenchima area.
- Select ROIs based on anatomical landmarks
- Use a similar anatomical region

[Example images of ROIs]

## Image size

Our model can accomodate differennt image sizes. The minimum size should be (128 x 128 x 128) pixels, which is the size of the neural network receptive field. Bigger images are processed in tiles. At the scan resolution used for training the model (which is [xxx]), the size of ROIs around the lungs is about (300 x 300 x 300) pixels. Images of this size can be processed in less than 20 seconds on a modern GPU (e.g. RTX 3060).

## Intensity normalization

We apply a quantile-based intensity normalization to each image independently as a preprocessing step. We set the minimum and maximum intensities respectively at the 2nd and 98th percentile. This ensures that most of the graylevel intensities fall within the range 0-1. This preprocessing is done internally in the nnUNet model framework, which we have modified to integrate this preprocessing.

## Image orientation

The image axis order (ZYX, XYZ...) should not matter. We integrated random flipping, mirroring, and image transpose operations as augmentations during training.