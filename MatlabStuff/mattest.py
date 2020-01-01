import cv2
import numpy as np
from math import sqrt, floor, log2

def downscale(img, scale):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    return cv2.resize(img, (width, height))

A = cv2.imread('TestImages/Nashville/Frame17.png')
A = downscale(A, .1)
gray = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
cv2.imshow("Image", A)

height = A.shape[0]
width = A.shape[1]

wavelengthMin = 4/sqrt(2)
wavelengthMax = sqrt(height**2 + width**2)
n = floor(log2(wavelengthMax/wavelengthMin))
wavelength = np.arange(0, n-1)
wavelength = 2.0 ** wavelength
wavelength = wavelength * wavelengthMin
print(wavelength)

orientation = np.arange(0, 180, 45)

print(wavelength, orientation)