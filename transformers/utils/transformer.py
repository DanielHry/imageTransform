# -*- coding: utf-8 -*-
import cv2
import numpy as np

from .util import createLargeImage, get_rad


def imageTransformer(image, theta=0, phi=0, gamma=0, dx=0, dy=0, dz=0, bordMode=cv2.BORDER_CONSTANT):
    
    """ Get radius of rotation along 3 axes """
    rtheta, rphi, rgamma = get_rad(theta, phi, gamma)
    
    """ Image Parameters """
    height, width = image.shape[:2]
    imageLarge = createLargeImage(image.copy())
    hLarge, wLarge = imageLarge.shape[:2] 
    
    """ Create Image with White Conturs """
    border = 1
    imageBorder = cv2.copyMakeBorder(image.copy(), border, border, border, border, cv2.BORDER_CONSTANT, value=(255,255,255))
    imageLargeBorder = createLargeImage(imageBorder.copy())
    hLargeBorder, wLargeBorder = imageLargeBorder.shape[:2]
    
    """ Get ideal focal length on z axis """
    d = np.sqrt(hLargeBorder**2 + wLargeBorder**2)
    focal = d / (2 * np.sin(rgamma) if np.sin(rgamma) != 0 else 1)
    if gamma>=0:
        dz = focal + dz
    if gamma<0:
        dz = focal - dz
        
    """ Get projection matrix """
    matImage = get_M(rtheta, rphi, rgamma, dx, dy, dz, focal, width, height)
    matImageLarge = get_M(rtheta, rphi, rgamma, dx, dy, dz, focal, wLarge, hLarge)
        
    """ Wrap Images """
    imgPerspLarge = cv2.warpPerspective(imageLarge, matImageLarge,
                                        (wLarge, hLarge), borderMode=bordMode)
    imgPerspLargeBorder = cv2.warpPerspective(imageLargeBorder, matImageLarge,
                                              (wLargeBorder, hLargeBorder), borderMode=bordMode)
    
    return imgPerspLarge, imgPerspLargeBorder, matImage



def get_M(theta, phi, gamma, dx, dy, dz, focal, width, height):
    """ Get Perspective Projection Matrix """
        
    w = width
    h = height
    f = focal
    # Projection 2D -> 3D matrix
    A1 = np.array([ [1, 0, -w/2],
                    [0, 1, -h/2],
                    [0, 0, 1],
                    [0, 0, 1]])
    # Rotation matrices around the X, Y, and Z axis
    RX = np.array([ [1, 0, 0, 0],
                    [0, np.cos(theta), -np.sin(theta), 0],
                    [0, np.sin(theta), np.cos(theta), 0],
                    [0, 0, 0, 1]])
    RY = np.array([ [np.cos(phi), 0, -np.sin(phi), 0],
                    [0, 1, 0, 0],
                    [np.sin(phi), 0, np.cos(phi), 0],
                    [0, 0, 0, 1]])
    RZ = np.array([ [np.cos(gamma), -np.sin(gamma), 0, 0],
                    [np.sin(gamma), np.cos(gamma), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
    # Composed rotation matrix with (RX, RY, RZ)
    R = np.dot(np.dot(RX, RY), RZ)
    # Translation matrix
    T = np.array([  [1, 0, 0, dx],
                    [0, 1, 0, dy],
                    [0, 0, 1, dz],
                    [0, 0, 0, 1]])
    # Projection 3D -> 2D matrix
    A2 = np.array([ [f, 0, w/2, 0],
                    [0, f, h/2, 0],
                    [0, 0, 1, 0]])
    # Final transformation matrix
    return np.dot(A2, np.dot(T, np.dot(R, A1)))


def resize_poly(points, imgSize, imgSizeTr):
    """ Resize polyon points """
    
    h_scale = imgSize[0] / imgSizeTr[0]
    w_scale = imgSize[1] / imgSizeTr[1]
    new_box = []
    for n, i in enumerate(points):
        if n%2 == 0:
            new_box.append(int(i/w_scale))
        else:
            new_box.append(int(i/h_scale))
    return new_box


def translate_poly(points, h, w):
    """ Translate polyon points """
    
    new_points = []
    for n, p in enumerate(points):
        if n % 2 == 0:
            new_points.append(p+w)
        else:
            new_points.append(p+h)
    return new_points


def rotate_poly(points, M):
    """ Rotate 3D polygon points """
    
    points = np.array(points).reshape((-1,1,2))
    homg_points = np.array([[x, y, 1] for [[x, y]] in points]).T
    transf_homg_points = M.dot(homg_points)
    transf_homg_points /= transf_homg_points[2]
    transf_points = np.array([[[x,y]] for [x, y] in transf_homg_points[:2].T])
    transf_points = transf_points.reshape(1,-1).astype(np.int32)[0]
    return transf_points