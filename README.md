# Modern CRAFT Library

## Overview
This Python library provides an interface for using the CRAFT (Character Region Awareness For Text Detection) algorithm for text detection in images. The library is based on the CRAFT implementation in Python.

This is an adaptation of the CRAFT-python library allowing for use on modern packages (pytorch 2 > opencv-python > 3.4).

## ToDo
This library will need refactoring with respect to performance as the previous library introduced unneeded overhead.


## Requirements
- Python 3.x
- PyTorch
- OpenCV
- NumPy

## Installation
You can install the library via pip:


```
pip install modern-craft
```

## Usage

```
    from mcraft import TNet
    
    # Load an image
    image_path = "path/to/your/image.jpg"
    
    # Initialize the network
    tnet = TNet()  # Adjust parameters as needed
    
    # Run a test
    tnet.test(image_path)
    
    # Perform text detection
    tnet.test(image_path)
    
    # After running test, the result will be saved as "res_image_mask.jpg" in the same directory as the input image
```

## Features
- Text detection in images produced as heat-maps bounding boxes and per-character polygons.
- Adjustable parameters such as text threshold, link threshold, etc.

## Important Notes
- Preexisting or hand compiled instances of opencv, pytorch, and torchvision will **not** be replaced during setup.
- The necessary model files (`craft_mlt_25k.pth` and `craft_refiner_CTW1500.pth`) will be downloaded to ~/.cache/mcraft.
- GPU operations, whilst implemented, remain untested until I get back from abroad and regain access to my compute systems.
