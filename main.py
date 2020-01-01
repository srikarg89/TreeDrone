import cv2
import numpy as np
from skimage.filters import gabor

PROCESS_DIM = (1280, 720)
DISPLAY_DIM = (1280 // 3, 720 // 3)

def gabor_filter(img, frequency):
    filt_real, filt_imag = gabor(img, frequency=.6)
    return filt_real

def resize(img, dim):
    return cv2.resize(img, dim)

def displayVstack(title, imgs):
    vstack = cv2.vconcat([resize(img, DISPLAY_DIM) for img in imgs])
    cv2.imshow(title, vstack)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def bgr2hsv(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def gaussianblur(img, kernel=(5,5)):
    return cv2.GaussianBlur(img,kernel,0)

def run(img):
    gray = grayscale(img)
#    blur = gaussianblur(gray)
    gabor = gabor_filter(gray, frequency=0.6)
    gabor = closing(gabor, kernel=(5,5), iterations=5)
    gabor = opening(gabor, kernel=(5,5), iterations=3)
#    gabor = closing(gabor, kernel=(2,2), iterations=3)
#    gabor = opening(gabor, kernel=(2,2), iterations=1)
    return gabor

def opening(img, kernel=(5,5), iterations=1):
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=iterations)

def closing(img, kernel=(5,5), iterations=1):
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=iterations)

def dilate(img, kernel=(5,5), iterations=1):
    return cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel, iterations=iterations)

def erode(img, kernel=(5,5), iterations=1):
    return cv2.morphologyEx(img, cv2.MORPH_ERODE, kernel, iterations=iterations)

def run_through_images(func, image_names, imdir='', ext='.png'):
    for name in image_names:
        img = cv2.imread(imdir + name + ext)
        img = resize(img, PROCESS_DIM)
        new = func(img)
#        vstack = cv2.vconcat([img, new])
        new = cv2.cvtColor(new, cv2.COLOR_GRAY2BGR)
        displayVstack('Image: ' + name, [img, new])

def inrange(img, range1, range2):
    return cv2.inRange(img, range1, range2)

def test():
    img = cv2.imread('TestImages/Nashville/Frame30.png')
    img = resize(img, PROCESS_DIM)
    hsv = bgr2hsv(img)
    new = inrange(hsv, (50,0,0), (90,255,255))
#    new = closing(new, kernel=(4,4), iterations=10)
#    new = inrange(img, (0,150,0), (255,255,255))
#    new = cv2.cvtColor(new, cv2.COLOR_GRAY2BGR)
    displayVstack('InRange', [img, new])
#    cv2.imshow("New", new)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()

#test()
imdir = 'TestImages/Nashville/'
names = ['Frame' + str(i) for i in range(0,234,10)]
run_through_images(run, names, imdir)