from numpy import array, random
import numpy as np
from scipy.cluster.vq import kmeans2
import matplotlib.pyplot as plt

#features  = array([[ 1.9,2.3],
#                    [ 1.5,2.5],
#                    [ 0.8,0.6],
#                    [ 0.4,1.8],
#                    [ 0.1,0.1],
#                    [ 0.2,1.8],
#                    [ 2.0,0.5],
#                    [ 0.3,1.5],
#                    [ 1.0,1.0]])
npfile_dir = 'Numpy_files/'
features = np.load(npfile_dir + 'SafewayGabor1.npy')

#whitened = whiten(features)
#book = array((whitened[0],whitened[2]))
#print(kmeans(whitened, book))

#pts = 50
#a = np.random.multivariate_normal([0, 0], [[4, 1], [1, 4]], size=pts)
#b = np.random.multivariate_normal([30, 10],
#                                   [[10, 2], [2, 1]],
#                                   size=pts)

#features = np.concatenate((a, b))

# Whiten data
#whitened = whiten(features)
#print(whitened[0])

import cv2
img = cv2.imread("../TestFrame.png")
img = cv2.resize(img, (img.shape[1] // 4, img.shape[0] // 4))
features = img.reshape((img.shape[0] * img.shape[1], 3))
print(features.shape)
features = features.astype('float64')

# Find 2 clusters in the data
centroid, label = kmeans2(features, 3, minit='points')
print(centroid)
counts = np.bincount(label)
print(counts)

features = features.astype('uint8')
mask = np.zeros(features.shape).astype('uint8')
mask[label == 0] = 255
w0 = np.bitwise_and(features, mask)
mask[label == 0] = 0
mask[label == 1] = 255
w1 = np.bitwise_and(features, mask)
mask[label == 1] = 0
mask[label == 2] = 255
w2 = np.bitwise_and(features, mask)

w0 = np.reshape(w0, img.shape)
w1 = np.reshape(w1, img.shape)
w2 = np.reshape(w2, img.shape)

print(w0.shape, w1.shape, w2.shape)

cv2.imshow("Kmeans1", w0)
cv2.imshow("Kmeans2", w1)
cv2.imshow("Kmeans3", w2)
cv2.waitKey(0)
cv2.destroyAllWindows()

#codebook, distortion = kmeans2(whitened, 3)
#print(codebook[0], codebook[1])
# Plot whitened data and cluster centers in red
#plt.scatter(whitened[:, 0], whitened[:, 1])
#plt.scatter(codebook[:, 0], codebook[:, 1], c='r')
#plt.show()