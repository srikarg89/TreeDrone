import numpy as np
import cv2

shape = (288,512,26)

npfile_dir = 'Numpy_files/'
gabor_output = np.load(npfile_dir + 'Safeway11.npy')
print(gabor_output.shape)
#gabor_output = gabor_output.reshape(shape)
np.savetxt('CSV_files/Safeway11.csv', gabor_output, delimiter=',')
#cv2.imwrite("Images/Gaborfilter.png", gabor_output)
