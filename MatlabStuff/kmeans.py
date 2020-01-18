from numpy import array, random
import numpy as np
from scipy.cluster.vq import vq, kmeans, whiten
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

pts = 50
a = np.random.multivariate_normal([0, 0], [[4, 1], [1, 4]], size=pts)
b = np.random.multivariate_normal([30, 10],
                                   [[10, 2], [2, 1]],
                                   size=pts)

#features = np.concatenate((a, b))

# Whiten data
whitened = whiten(features)
print(whitened[0])

# Find 2 clusters in the data
codebook, distortion = kmeans(whitened, 3)
print(codebook[0], codebook[1])
# Plot whitened data and cluster centers in red
#plt.scatter(whitened[:, 0], whitened[:, 1])
plt.scatter(codebook[:, 0], codebook[:, 1], c='r')
plt.show()