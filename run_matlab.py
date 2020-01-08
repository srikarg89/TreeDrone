import matlab.engine
import scipy.io
import numpy as np

eng = matlab.engine.start_matlab()
print("Whatsup")
ret = eng.texture_segmentation('TestImages/Nearby/Frame17_undistorted.png', nargout=3)

for i,img in enumerate(ret):
    print(img.size)
    np_a = np.array(img._data.tolist())
    np_a = np_a.reshape(img.size[::-1]).transpose()
    print(np_a.shape)
    np.save('imgfile' + str(i + 1), np_a)