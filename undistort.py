import cv2
import numpy as np
import sys

DISPLAY_DIM = (1280 // 3, 720 // 3)

# You should replace these 3 lines with the output in calibration step
DIM=(1920, 1080)
K=np.array([[1163.9735109252772, 0.0, 969.3772594176671], [0.0, 1186.1636133671516, 511.7440041531628], [0.0, 0.0, 1.0]])
D=np.array([[-0.09359524859164836], [0.028174415309667373], [-0.055340807338124354], [0.0314309698675567]])

def displayVstack(title, imgs):
    vstack = cv2.vconcat([cv2.resize(img, DISPLAY_DIM) for img in imgs])
    cv2.imshow(title, vstack)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def undistort(img_path, balance=0.0, dim2=None, dim3=None):
    img = cv2.imread(img_path)
    dim1 = img.shape[:2][::-1]  #dim1 is the dimension of input image to un-distort
    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1
    scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0
    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
#    print(undistorted_img.shape)
#    ori = cv2.resize(undistorted_img, (1920 // 3, 1080 // 3))
#    displayVstack("Images", [img, undistorted_img])
#    cv2.imshow("original", ori)
#    cv2.imshow("undistorted", undistorted_img)
#    cv2.waitKey(0)
#    cv2.destroyAllWindows()
    return undistorted_img

if __name__ == '__main__':
    folder = 'TestImages/Nearby/'
    filename = 'Frame17.png'
    newname = 'Frame17_undistorted.png'
    newimg = undistort(folder + filename)
    cv2.imwrite(folder + newname, newimg)
#    filenames = ['Frame54.png', 'Frame60.png', 'Frame62.png']
#    for filename in filenames:
#        newimg = undistort(folder + filename)
#        cv2.imwrite(folder + filename, newimg)