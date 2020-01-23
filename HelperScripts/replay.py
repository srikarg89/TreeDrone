import cv2

cap = cv2.VideoCapture('Videos/Flight1/Drone/GL_20200102_161514.mp4')
cap2 = cv2.VideoCapture('Videos/Flight1/Phone/Phone-1_2_161452_Trim.mp4')
i = 0
inarow = 0

while cap.isOpened():
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()
#    print(frame.shape, frame2.shape)
    frame = cv2.resize(frame, (1920 // 4, 1080 // 4))
    frame2 = cv2.resize(frame2, (1920 // 4, 1080 // 4))
#    print(i, ret, ret2)
    if ret and ret2:
        inarow = 0
        cv2.imshow("Drone", frame)
        cv2.imshow("Phone", frame2)
    else:
        inarow += 1
        if inarow == 10:
            break
    if cv2.waitKey(1) == ord('q'):
        break
    i += 1

cap.release()