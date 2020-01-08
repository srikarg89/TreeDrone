import matlab.engine
import scipy.io
import numpy as np

eng = matlab.engine.start_matlab()
print("Whatsup")
tf = eng.texture_segmentation()
print(type(tf))
print(len(tf))
print(len(tf[0]))
print(len(tf[0][0]))
print(tf.size)
np_a = np.array(tf._data.tolist())
np_a = np_a.reshape(tf.size)
print(np_a.shape)
np.save('imgfile', np_a)