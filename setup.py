from setuptools import setup
import os.path

_dir = os.path.dirname(__file__)

with open(os.path.join(_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='mousetumornet',
    packages=["mousetumornet"],
    version='0.0.1',
    description='nnU-Net model for the segmentation of lung tumor nodules in mice CT scans.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.epfl.ch/center-for-imaging/mousetumornet',
    author='Center for Imaging, Ecole Polytechnique Federale de Lausanne (EPFL)',
    author_email='mallory.wittwer@epfl.ch',
    license='BSD 3-Clause License',
    python_requires=">3.9, <3.11",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        # "Framework :: napari",
    ],
    install_requires=[
        "nnunetv2",
        "napari-label-focus",
        "pooch"
    ],
    extras_require={
        "test": ["pytest"],
    },
    entry_points={
        'napari.manifest': ['mousetumornet = mousetumornet:napari.yaml'],
        'console_scripts': [
            'mtn_predict_image = mousetumornet.cli:cli_predict_image',
            'mtn_predict_folder = mousetumornet.cli:cli_predict_folder',
            'mtn_extract_roi = mousetumornet.cli:cli_extract_roi',
        ],
    },
    keywords=['deep learning', 'image segmentation', 'nnU-Net', 'nnunet']
)
