# -*- coding: utf-8 -*-
import sys
import cv2
import numpy as np

from .utils.transformer import imageTransformer
from .polygones import translate_poly, transform_M_poly
from .utils.util import getBbox


def rotate_layer(layers, dictRotation):
    """Rotate Layers.
    
    Args:
        layers (list[ndarray]): list with the input images.
        dictRotation (dict): keys & values:
            'theta' : int  # rotation around the x axis.
            'phi' : int    # rotation around the y axis.
            'gamma' : int  # rotation around the z axis.
            
    Return:
        list[ndarray] : list of image rotated
    
    """
    global imgBiggerSize, imgOriginalSize, M, imageCroped, hTr, wTr, p
    
    theta = dictRotation['theta']    # rotation around the x axis
    phi   = dictRotation['phi']      # rotation around the y axis
    gamma = dictRotation['gamma']    # rotation around the z axis
    
    if len(layers) > 1:
        result = all(elem.shape == layers[0].shape for elem in layers)
        if not result:
            print("All images must have the same shape")
            sys.exit()
    

    transformedImages = []
    for n, img in enumerate(layers):
        
        # Rotate Image
        image, imgPerspLargeBorder, M = imageTransformer(img, theta, phi, gamma)
        
        if n == 0:
            # Get Image perfect size
            imgBiggerSize = image.shape[:2]
            imgOriginalSize = img.shape[:2]
            hTr, wTr = getBbox(imgPerspLargeBorder)
            hSt, wSt = getBbox(np.flip(imgPerspLargeBorder))
            p = 2
            
        # Crop Image
        imageCroped = image[hTr-p: imgBiggerSize[0] - hSt+p, wTr-p: imgBiggerSize[1] - wSt+p]
        imageCroped = cv2.copyMakeBorder(imageCroped.copy(), 1,1,1,1, cv2.BORDER_CONSTANT, value=(0,0,0))
        transformedImages.append(imageCroped)
        
    return transformedImages

             
                                   
def rotate_poly(polygone):
    """Rotate Polygone.
    
    Args:
        polygone (list): The input polygone [x1,y1,x2,y2,x3,y3,x4,y4].
            
    Return:
        list: polygone [x1,y1,x2,y2,x3,y3,x4,y4]
    
    """    
    # Rotate
    transf_points = transform_M_poly(polygone, M)
    # Translate Bigger
    hh = round(imgBiggerSize[0]/4)
    ww = round(imgBiggerSize[1]/4)
    transf_points = translate_poly(transf_points, hh, ww)
    # Crop 
    transf_points = translate_poly(transf_points, -hTr+p, -wTr+p)
    return transf_points



def get_mask():
    """Create a mask of rotate layer.
                
    Return:
        ndarray: Image mask
    """
    # Get Image Rectangle
    height, width = imgOriginalSize
    pointsMask = np.array([0,0,width,0,width,height,0,height])
    pointsMask = rotate_poly(pointsMask)
    # Create empty image
    mask = np.zeros_like(imageCroped)
    # Create Mask
    pointsMask = np.array(pointsMask).reshape((-1,1,2))
    mask = cv2.fillPoly(mask, pts=[pointsMask], color=(255,255,255))
    return mask
    
    