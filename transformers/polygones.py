# -*- coding: utf-8 -*-
import numpy as np


def resize_poly(polygone, scale):
    """Resize polygones target scale height & scale width.

    Args:
        polygone (list): The input polygone [x1,y1,x2,y2,x3,y3,x4,y4].
        scale (float): Target scale.
        
    Return:
        list: 'resize_poly' [x1,y1,x2,y2,x3,y3,x4,y4]
    """
    res_poly = []
    for n, i in enumerate(polygone):
        if n % 2 == 0:
            res_poly.append(round(i * scale))
        else:
            res_poly.append(round(i * scale))
    return res_poly



def translate_poly(polygone, y=0, x=0):
    """Translate polygones target height & width.

    Args:
        polygone (list): The input polygone [x1,y1,x2,y2,x3,y3,x4,y4].
        y (float): translate with vertical axis.
        x (float): translate with horizontal axis.
        
    Return:
        list: 'tr_poly' [x1,y1,x2,y2,x3,y3,x4,y4]
    """
    tr_poly = []
    for n, p in enumerate(polygone):
        if n % 2 == 0:
            tr_poly.append(p + x)
        else:
            tr_poly.append(p + y)
    return tr_poly



def transform_M_poly(polygone, M):
    """Transform polygone points with 3D Matrix.

    Args:
        polygone (list): The input polygone [x1,y1,x2,y2,x3,y3,x4,y4].
        M (ndarray): The transform matrix with dtype float32
        
    Return:
        list: 'tr_poly' [x1,y1,x2,y2,x3,y3,x4,y4]
    """
    polygone = np.array(polygone).reshape((-1,1,2))
    homg_points = np.array([[x, y, 1] for [[x, y]] in polygone]).T
    transf_homg_points = M.dot(homg_points)
    transf_homg_points /= transf_homg_points[2]
    tr_poly = np.array([[[x,y]] for [x, y] in transf_homg_points[:2].T])
    tr_poly = tr_poly.reshape(1,-1).astype(np.int32)[0]
    return tr_poly



def flip_poly(polygon, layer, direction="horizontal"):
    """Flip polygone points.
    
    Args:
        polygone (list): The input polygone [x1,y1,x2,y2,x3,y3,x4,y4].
        layer (ndarray): The input image
        direction (str): The flip direction, either
            "horizontal" or "vertical" or "diagonal".
        
    Return:
        list: polygone [x1,y1,x2,y2,x3,y3,x4,y4]
    """
    def for_p(poly, h, w, x=True, y=False):
        trans_poly = []
        for n, p in enumerate(poly):
            if n % 2 == 0:
                if x:
                    trans_poly.append(w - p)
                else:
                    trans_poly.append(p)
            else:
                if y:
                    trans_poly.append(h - p)
                else:
                    trans_poly.append(p)
        return trans_poly
    
    h, w = layer.shape[:2]
    if direction == "horizontal":
        return for_p(polygon, h, w, x=True, y=False)
    elif direction == "vertical":
        return for_p(polygon, h, w, x=False, y=True)
    elif direction == "diagonal":
        return for_p(polygon, h, w, x=True, y=True)
    else:
        return polygon






