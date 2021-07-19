# -*- coding: utf-8 -*-
import cv2
import numpy as np

from math import pi


def getBbox(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    for n, row in enumerate(image):
        if np.mean(row) > 0:
            heightStart = n
            break
    for n, row in enumerate(image.T):
        if np.mean(row) > 0:
            widthStart = n
            break
    return heightStart, widthStart


def createLargeImage(image):
    """ Create x2 Larger image """
    h, w = image.shape[:2]
    newImage = np.zeros((h*2, w*2, 3), dtype=np.uint8)
    """ Center Image """
    newH, newW = newImage.shape[:2]
    newImage[round(h/2):h+round(h/2), round(w/2):w+round(w/2)] = image
    return newImage

def get_rad(theta, phi, gamma):
    return (deg_to_rad(theta),
            deg_to_rad(phi),
            deg_to_rad(gamma))

def get_deg(rtheta, rphi, rgamma):
    return (rad_to_deg(rtheta),
            rad_to_deg(rphi),
            rad_to_deg(rgamma))

def deg_to_rad(deg):
    return deg * pi / 180.0

def rad_to_deg(rad):
    return rad * 180.0 / pi