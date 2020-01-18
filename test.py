import cv2

vid = cv2.VideoCapture('D:/video/20200112-160256-704278-0.avi')
framecount = 0
while vid.isOpened():
    ret, frame = vid.read()
    if ret == False:
        continue
    framecount += 1
    if framecount % 20 == 0:
        print(framecount)
    if framecount == 200:
        cv2.imshow("Image", cv2.resize(frame, (3840 // 6, 2160 // 6)))
        cv2.imwrite("TestFrame.jpg", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        break

vid.close()