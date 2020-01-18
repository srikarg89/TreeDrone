import numpy as np
import cv2

#npfile_dir = 'MatlabStuff/Numpy_files/Nashville_'
npfile_dir = 'Numpy_files/'
imgfile_dir = 'Images/Safeway1_'

img1 = np.load(npfile_dir + 'Safeway11.npy')
img2 = np.load(npfile_dir + 'Safeway12.npy')
img3 = np.load(npfile_dir + 'Safeway13.npy')

img1 = img1.astype('uint8')
img2 = img2.astype('uint8')
img3 = img3.astype('uint8')

img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
img3 = cv2.cvtColor(img3, cv2.COLOR_RGB2GRAY)

cv2.imwrite(imgfile_dir + "Image1.png", img1)
cv2.imwrite(imgfile_dir + "Image2.png", img2)
cv2.imwrite(imgfile_dir + "Image3.png", img3)