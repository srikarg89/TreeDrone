import cv2
import os

#filename = "WindsorNationalPark"
filename = "Nashville"
#ending = ".mp4"
ending = ".webm"
savename = "Frame"
os.mkdir("TestImages/" + filename)
cap = cv2.VideoCapture("Videos/" + filename + ending)

fails = 0
framenum = 0
saverate = 50
while cap.isOpened():
    if fails == 100:
        break
    ret, frame = cap.read()
    if ret:
        if framenum % saverate == 0:
            print(framenum)
            cv2.imwrite("TestImages/" + filename + "/" + savename + str(framenum // saverate) + ".png", frame)
        fails = 0
        framenum += 1
    else:
        fails += 1

cap.release()