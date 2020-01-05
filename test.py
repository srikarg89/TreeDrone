import cv2

img = cv2.imread("C:/Users/Srikar/Downloads/testimg3.jpg")

global mouseX, mouseY
mouseX, mouseY = 0, 0

def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),10,(255,0,0),2)
        mouseX,mouseY = x,y

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

print(img.shape)
img = cv2.resize(img, (3840 // 4, 2160 // 4))

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        print(mouseX, mouseY)
    elif k == ord('q'):
        cv2.destroyAllWindows()
        break

# 149 = 10 in.
# 169 = 11.3 in.