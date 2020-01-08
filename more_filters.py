import cv2

img = cv2.imread("Image2.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, (6,6), iterations=5)
applied = cv2.bitwise_and(img, img, mask=mask)

#cv2.imwrite("Image4.png", applied)
hsv = cv2.cvtColor(applied, cv2.COLOR_BGR2HSV)

cv2.imshow("Image", hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()