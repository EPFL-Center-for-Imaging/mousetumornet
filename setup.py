from setuptools import setup, find_namespace_packages

setup(
    name='mousetumornet',
    packages=find_namespace_packages(include=[
        "mousetumornet", 
        "mousetumornet.*",
      ]),
    version='0.0.1',
    description='nnU-Net model for the segmentation of lung tumor nodules in mice CT scans.',
    url='https://gitlab.epfl.ch/center-for-imaging/mousetumornet',
    author='Center for Imaging, Ecole Polytechnique Federale de Lausanne (EPFL)',
    author_email='mallory.wittwer@epfl.ch',
    license='BSD 3-Clause License',
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Framework :: napari",
    ],
    install_requires=[
        "nnunetv2 @ git+https://github.com/MalloryWittwer/nnUNet.git",
        "napari_label_focus @ git+https://github.com/MalloryWittwer/napari-label-focus.git",
        "napari[all]>=0.4.16", 
        "napari-tools-menu",
        "napari-workflows",
        "pooch"
    ],
    entry_points={
        'napari.manifest': ['mousetumornet = mousetumornet:napari.yaml'],
        'console_scripts': [
            'mousetumornetnet_predict_image = mousetumornet.nnunet_predict:cli_predict_image',
            'mousetumornetnet_predict_folder = mousetumornet.nnunet_predict:cli_predict_folder',
        ],
    },
    keywords=['deep learning', 'image segmentation', 'nnU-Net', 'nnunet']
)
