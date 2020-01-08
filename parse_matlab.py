import numpy as np
import cv2

img = np.load('imgfile.npy')
print(img.shape)
img = img.transpose()
print(img.shape)
#img1 = img[0]
#img2 = img[1]
#img3 = img[2]

#shape = (img.shape[2], img.shape[1], 1)
#img1 = img1.reshape(shape)
#img2 = img2.reshape(shape)
#img3 = img3.reshape(shape)

#img = np.concatenate((img1, img2, img3), axis=2)

cv2.imwrite('Mask.png', img)

#cv2.imwrite("Mask1.png", img1)
#cv2.imwrite("Mask2.png", img2)
#cv2.imwrite("Mask3.png", img3)