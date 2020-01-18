import cv2

img = cv2.imread("Image2.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, (6,6), iterations=5)
img = cv2.bitwise_and(img, img, mask=mask)

#cv2.imwrite("Image4.png", applied)
#hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

def ganesh_filter(img, kernel = (3,3)):
    diff = (kernel // 2, kernel // 2)
    cache = {}
    width = len(img) // kernel[0]
    height = len(img[0]) // kernel[1]
    for i in range(width):
        x = diff[0] + kernel[0] * i
        for j in range(height):
            y = diff[1] + kernel[1] * j

laplacian = cv2.Laplacian(img, cv2.CV_64F)
sobelx = cv2.Sobel(img, cv2.CV_64F,1,0,ksize=5)
sobely = cv2.Sobel(img, cv2.CV_64F,0,1,ksize=5)

from matplotlib import pyplot as plt

plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,2),plt.imshow(laplacian,cmap = 'gray')
plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(sobelx,cmap = 'gray')
plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,4),plt.imshow(sobely,cmap = 'gray')
plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

plt.show()

#cv2.imshow("Image", img)
#cv2.imshow("Laplacian", laplacian)
#cv2.imshow("Sobel X", sobelx)
#cv2.imshow("Sobel Y", sobely)
#cv2.waitKey(0)
#cv2.destroyAllWindows()