from scipy.cluster.vq import kmeans2
import numpy as np
import cv2


# Find 2 clusters in the data
features = np.load("GaborSpace.npy")
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

w0 = np.reshape(w0, features.shape)
w1 = np.reshape(w1, features.shape)
w2 = np.reshape(w2, features.shape)

print(w0.shape, w1.shape, w2.shape)

cv2.imshow("Kmeans1", w0)
cv2.imshow("Kmeans2", w1)
cv2.imshow("Kmeans3", w2)

cv2.imwrite("Kmeans1.png", w0)
cv2.imwrite("Kmeans2.png", w1)
cv2.imwrite("Kmeans3.png", w2)

cv2.waitKey(0)
cv2.destroyAllWindows()
