# -*- coding: utf-8 -*-
import numpy as np
import cv2

from .layers import crop_layer


def blend_layers(layerA, layerB, mask=None, position=(0,0), opacity=1.0):
    """Blend two layers
    
    Args:
        layerA (ndarray): The input image forground.
        layerB (ndarray): The input image background.
        mask (ndarray) or None: The input image forground mask.
        position (tuple[int]): 'layerA' position (x, y).
        opacity (float): 'LayerA' opacity, betwen 0 - 1.
    
    Return:
        ndarray : image outpout.
    """
    
    x, y = position
    hA, wA = layerA.shape[:2]
    hB, wB = layerB.shape[:2]
    
    """ Check mask """
    if mask is None:
        mask = np.zeros((hA, wA), dtype=np.uint8)+255
    if len(mask.shape) != 3:
            mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    
    """ Crop layer """
    if x + wA > wB:
        right = wB - (x + wA)
    else:
        right = 0
    if y + hA > hB:
        bottom = hB - (y + hA)
    else:
        bottom = 0
    if x < 0 :
        left = abs(x)
        x = 0
    else:
        left = 0
    if y < 0 :
        top = abs(y)
        y = 0
    else:
        top = 0
    layerA = crop_layer(layerA, left=left, right=right, top=top, bottom=bottom)
    mask = crop_layer(mask, left=left, right=right, top=top, bottom=bottom)
    position = (x, y)

    
    """ Opacity """
    op = 255 - round(255 * opacity)
    mask = cv2.subtract(mask, np.zeros_like(mask)+op)


    """ Crop Roy Image """
    def image_roy(image, shape, position):
        x, y = position
        h, w = shape
        roy = image[y:y+h, x:x+w]
        return roy
        
    
    """ Blend with mask """
    def blend(layerA, layerB, mask):
        img_res = (mask/255 * layerA) + ((255 - mask)/255 * layerB)
        return img_res.astype(np.uint8)

    h, w = layerA.shape[:2]
    roy = image_roy(layerB, (h, w), position)
    roy_blend = blend(layerA, roy, mask)
    layerB[y:y+h, x:x+w] = roy_blend
    
    return layerB
