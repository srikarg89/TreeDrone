import cv2
import numpy as np

def resize(img, dim):
    return cv2.resize(img, dim)

display_dim = (3840 // 6, 2160 // 6)
img = cv2.imread('TestImages/Nashville/Frame17.png')
img = resize(img, display_dim)
print(img.shape)
#print(1/0)
#print(img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
euclid = lab[:, :, 0]
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hue = hsv[:, :, 0]
sat = hsv[:, :, 1]
val = hsv[:, :, 2]

_, highsat = cv2.threshold(sat, 170, 255, cv2.THRESH_BINARY)

print(gray.shape, lab.shape, hsv.shape)

cv2.imshow("Original", img)
#cv2.imshow("Gray", gray)
#cv2.imshow("Lab", lab)
#cv2.imshow("Euclidian Distance", euclid)
#cv2.imshow("HSV", hsv)
#cv2.imshow("Hue", hue)
cv2.imshow("Saturation", sat)
cv2.imshow("High saturation", highsat)
#cv2.imshow("Val", val)
cv2.waitKey(0)