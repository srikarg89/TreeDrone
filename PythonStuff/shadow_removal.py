import cv2
import numpy as np

def hsv_method():
    img = cv2.imread("TestImages/Nashville/Frame142.png")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    print(hsv.shape)
    avg_value = np.sum(np.sum(hsv, axis=1), axis=0)[2] / (len(hsv) * len(hsv[0]))
    print(avg_value)
    hsv[:,:,1] = avg_value
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    cv2.imshow("HSV", cv2.resize(hsv, (3840 // 6, 2160 // 6)))
    cv2.imshow("BGR", cv2.resize(bgr, (3840 // 6, 2160 // 6)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def online_method():
#    img = cv2.imread("TestImages/Nashville/Frame142.png", -1)
    img = cv2.imread("MatlabStuff/Images/Image4.png", -1)
    rgb_planes = cv2.split(img)

    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)

    result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)

    _, thresh = cv2.threshold(cv2.cvtColor(result_norm, cv2.COLOR_BGR2GRAY), 200, 255, cv2.THRESH_BINARY_INV)

    cv2.imshow('Image', cv2.resize(img, (3840 // 6, 2160 // 6)))
    cv2.imshow('Shadows_out', cv2.resize(result, (3840 // 6, 2160 // 6)))
    cv2.imshow('Shadows_out_norm', cv2.resize(result_norm, (3840 // 6, 2160 // 6)))
    cv2.imshow('Threshold', cv2.resize(thresh, (3840 // 6, 2160 // 6)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


#hsv_method()
online_method()