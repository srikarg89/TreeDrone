import cv2
import os

#filename = "Nashville"
#filename = 'Bush/vid3'
#filename = "Westgate1"
filename = "Westgate2"
ending = ".mp4"
savename = "Frame"
os.mkdir("TestImages/" + filename)
cap = cv2.VideoCapture("Videos/" + filename + ending)

fails = 0
framenum = 0
saverate = 5
while cap.isOpened():
    if fails == 100:
        break
    ret, frame = cap.read()
    if ret:
        if framenum % saverate == 0:
            print(framenum)
#            cv2.imwrite("TestImages/" + filename + "/" + savename + str(framenum // saverate) + ".png", frame)
#            cv2.imwrite("TestImages/Bush/" + savename + str(framenum // saverate) + ".png", frame)
            cv2.imwrite("TestImages/Westgate2/" + savename + str(framenum // saverate) + ".png", frame)
        fails = 0
        framenum += 1
    else:
        fails += 1

cap.release()

### Groups ###
# 54, 60, 62