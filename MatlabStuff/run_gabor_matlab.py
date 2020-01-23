import matlab.engine
import numpy as np
import scipy.io
import cv2

eng = matlab.engine.start_matlab()
ret = eng.texture_segmentation('../TestFrame.png', nargout=1)

gabor_space = np.array(ret._data.tolist())
gabor_space = gabor_space.reshape(ret.size[::-1]).transpose()
print(gabor_space.shape)
