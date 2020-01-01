#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import sys

def build_filters():
    filters = []
    ksize = 31
    for theta in np.arange(0, np.pi, np.pi / 6):
        kern = cv2.getGaborKernel( (ksize, ksize), 4.0, theta, 10.0, 0.5, 0)
        kern /= 1.5 * kern.sum()
        filters.append(kern)
    return filters


def process(img, filters):
    accum = np.zeros_like(img)
    for kern in filters:
        fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
        np.maximum(accum, fimg, accum)
    return accum

def downscale(img, scale):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    return cv2.resize(img, (width, height))

img = cv2.imread('TestImages/Nashville/Frame17.png')
img = downscale(img, .25)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
filters = build_filters()

res1 = process(img, filters)
cv2.imshow('Image', img)
cv2.imshow('result', res1)
cv2.waitKey(0)
cv2.destroyAllWindows()
