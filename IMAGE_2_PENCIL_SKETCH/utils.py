"""
Utility functions for image processing and pencil sketch conversion.

This module provides functions to convert images to pencil sketches using OpenCV
and helper functions to convert between OpenCV and PIL image formats.
"""

import cv2
import numpy as np
from PIL import Image
from typing import Union


def convert_to_sketch_cv2(image_path: str, blur_ksize: int = 21, scale: int = 256, gamma: float = 0.8) -> np.ndarray:
    """
    Convert an image to a pencil sketch using OpenCV.
    
    Args:
        image_path (str): Path to the input image file
        blur_ksize (int, optional): Kernel size for Gaussian blur. Must be odd and >= 1. Defaults to 21.
        scale (int, optional): Scale factor for division operation. Defaults to 256.
        gamma (float, optional): Gamma correction value for darkening. Values < 1 darken the image. Defaults to 0.8.
    
    Returns:
        np.ndarray: Grayscale pencil sketch as uint8 numpy array
    
    Raises:
        FileNotFoundError: If the image file cannot be read
        ValueError: If blur_ksize is not odd or less than 1
    """
    # Validate blur kernel size
    if blur_ksize < 1 or blur_ksize % 2 == 0:
        raise ValueError("blur_ksize must be odd and >= 1")
    
    # Read image from disk
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not read image from path: {image_path}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)
    
    # Create pencil sketch using division
    sketch = cv2.divide(gray, blurred, scale=scale)
    
    # Apply gamma correction to darken the sketch
    sketch = np.power(sketch / 255.0, gamma)
    sketch = (sketch * 255).astype('uint8')
    
    return sketch


def cv2_to_pil_gray(cv2_image: np.ndarray) -> Image.Image:
    """
    Convert OpenCV grayscale image to PIL Image.
    
    Args:
        cv2_image (np.ndarray): OpenCV grayscale image (2D array)
    
    Returns:
        Image.Image: PIL Image in grayscale mode
    """
    return Image.fromarray(cv2_image, mode='L')


def cv2_to_pil_bgr(cv2_image: np.ndarray) -> Image.Image:
    """
    Convert OpenCV BGR image to PIL RGB Image.
    
    Args:
        cv2_image (np.ndarray): OpenCV BGR image (3D array)
    
    Returns:
        Image.Image: PIL Image in RGB mode
    """
    # Convert BGR to RGB
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb_image, mode='RGB')
