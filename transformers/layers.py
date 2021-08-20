# -*- coding: utf-8 -*-
import cv2
import numpy as np


cv2_interpolation = {
    'nearest': cv2.INTER_NEAREST,
    'bilinear': cv2.INTER_LINEAR,
    'bicubic': cv2.INTER_CUBIC,
    'area': cv2.INTER_AREA,
    'lanczos': cv2.INTER_LANCZOS4
}


def new_layer(size, color):
    """Create new layer.

    Args:
        size (tuple[int]): Target size (w, h).
        color (tuple[int]): Target color (r, g, b), value betwen 0 - 255.

    Returns:
        ndarray: 'new_layer'
            
    """
    width, height = size
    r = np.zeros((height, width), dtype=np.uint8) + color[0]
    g = np.zeros((height, width), dtype=np.uint8) + color[1]
    b = np.zeros((height, width), dtype=np.uint8) + color[2]
    
    new_layer = np.dstack((r,g,b))
    
    return new_layer



def scale_layer(layer, scale, interpolation='area'):
    """Scale layer uniformly

    Args:
        layer (ndarray): The input image.
        scale (float): Target scale.
        interpolation (str): Interpolation method, accepted values are
            "nearest", "bilinear", "bicubic", "area", "lanczos" for 'cv2'

    Returns:
        ndarray: 'scaled_layer'     
    """    
    width = int(layer.shape[1] * scale)
    height = int(layer.shape[0] * scale)
    scaled_layer = cv2.resize(layer, (width, height), 
                              interpolation=cv2_interpolation[interpolation])
    return scaled_layer



def resize_layer(layer, size, interpolation='area', return_scale=False):
    """Resize layer target height & width.

    Args:
        layer (ndarray): The input image.
        size (tuple[int]): Target size (w, h).
        return_scale (bool): Whether to return 'w_scale' and 'h_scale'.
        interpolation (str): Interpolation method, accepted values are
            "nearest", "bilinear", "bicubic", "area", "lanczos" for 'cv2'

    Returns:
        ndarray: 'resized_layer' or
        tuple: ('resized_layer', 'w_scale', 'h_scale')
            
    """
    h, w = layer.shape[:2]
    resized_layer = cv2.resize(
            layer, size, interpolation=cv2_interpolation[interpolation])
    
    if not return_scale:
        return resized_layer
    else:
        w_scale = size[0] / w
        h_scale = size[1] / h
        return resized_layer, w_scale, h_scale



def resize_layer_like(layer, dst_layer, interpolation='area',
                      return_scale=False):
    """Resize layer target height & width.

    Args:
        layer (ndarray): The input image.
        dst_layer (ndarray): The target image.
        return_scale (bool): Whether to return 'w_scale' and 'h_scale'.
        interpolation (str): Interpolation method, accepted values are
            "nearest", "bilinear", "bicubic", "area", "lanczos" for 'cv2'

    Returns:
        ndarray: 'resized_layer' or
        tuple: ('resized_layer', 'w_scale', 'h_scale')
            
    """
    h, w = dst_layer.shape[:2]
    return resize_layer(layer, (w, h), interpolation, return_scale)



def crop_layer(layer, left=0, right=0, top=0, bottom=0):
    """Crop layer.

    Args:
        layer (ndarray): The input image.
        left (int): number of pixels to crop at the left of the image.
        right (int): number of pixels to crop at the right of the image.
        top (int): number of pixels to crop at the top of the image.
        bottom (int): number of pixels to crop at the bottom of the image.

    Returns:
        ndarray: 'crop_layer' 

    """
    h, w = layer.shape[:2]
    if top > h:
        top = h
    if bottom > h or bottom == 0:
        bottom = h
    if left > w:
        left = w
    if right > w or right == 0:
        right = w
        
    crop_layer = layer[top:bottom, left:right]
        
    return crop_layer



def flip_layer(layer, direction='horizontal'):
    """Flip layer horizontally or vertically.

    Args:
        layer (ndarray): The input image.
        direction (str): The flip direction, either
            "horizontal" or "vertical" or "diagonal".

    Returns:
        ndarray: The flipped image

    """
    
    if direction == 'horizontal':
        return cv2.flip(layer, 1)
    elif direction == 'vertical':
        return cv2.flip(layer, 0)
    elif direction == 'diagonal':
        return cv2.flip(layer, -1)
    else:
        return layer
    
    
    
    
    
    
    
    

