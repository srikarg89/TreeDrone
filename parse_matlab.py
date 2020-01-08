import numpy as np
import cv2

img1 = np.load('imgfile1.npy')
img2 = np.load('imgfile2.npy')
img3 = np.load('imgfile3.npy')

img1 = img1.astype('uint8')
img2 = img2.astype('uint8')
img3 = img3.astype('uint8')

img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
img3 = cv2.cvtColor(img3, cv2.COLOR_RGB2BGR)

cv2.imwrite("Image1.png", img1)
cv2.imwrite("Image2.png", img2)
cv2.imwrite("Image3.png", img3)