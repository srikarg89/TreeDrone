import os
import cv2
import numpy as np
import matlab.engine
from skimage.filters import gabor

PROCESS_DIM = (1280, 720)
DISPLAY_DIM = (1280 // 3, 720 // 3)
LOW_GREEN = [0,0,0]
HIGH_GREEN = [255,255,255]

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

def run_gabor(img):
    gray = grayscale(img)
#    blur = gaussianblur(gray)
    gabor = gabor_filter(gray, frequency=0.6)
    gabor = closing(gabor, kernel=(5,5), iterations=5)
    gabor = opening(gabor, kernel=(5,5), iterations=3)
#    gabor = closing(gabor, kernel=(2,2), iterations=3)
#    gabor = opening(gabor, kernel=(2,2), iterations=1)
    return gabor

def filter_green(img):
    LOW_GREEN = (0,140,0)
    HIGH_GREEN = (40,200,255)
    hsv = bgr2hsv(img)
    return inrange(hsv, LOW_GREEN, HIGH_GREEN)

def opening(img, kernel=(5,5), iterations=1):
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=iterations)

def closing(img, kernel=(5,5), iterations=1):
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=iterations)

def dilate(img, kernel=(5,5), iterations=1):
    return cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel, iterations=iterations)

def erode(img, kernel=(5,5), iterations=1):
    return cv2.morphologyEx(img, cv2.MORPH_ERODE, kernel, iterations=iterations)

def run_through_images(func, image_names, imdir=''):
    for name in image_names:
        print(imdir + name)
        img = cv2.imread(imdir + name)
        img = resize(img, PROCESS_DIM)
        new = func(img)
#        vstack = cv2.vconcat([img, new])
        new = cv2.cvtColor(new, cv2.COLOR_GRAY2BGR)
        displayVstack('Image: ' + name, [img, new])

def inrange(img, range1, range2):
    return cv2.inRange(img, range1, range2)

def preprocess(img_path):
    img = cv2.imread(img_path)
    img = resize(img, PROCESS_DIM)
    hsv = bgr2hsv(img)
    new = inrange(hsv, (0,140,0), (40,200,255))
    new = cv2.cvtColor(new, cv2.COLOR_GRAY2BGR)
    cv2.imwrite('PreprocessedMap.png', new)

def run_gabor_filter_matlab(img_path):
    eng = matlab.engine.start_matlab()
    ret = eng.texture_segmentation(img_path, nargout=1)
    gabor_space = np.array(ret._data.tolist())
    gabor_space = gabor_space.reshape(ret.size[::-1]).transpose()
    np.save('GaborSpace', gabor_space)

def main():
    preprocess('Map.png')
    run_gabor_filter_matlab('PreprocessedMap.png')

