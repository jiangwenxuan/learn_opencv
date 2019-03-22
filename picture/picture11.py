import cv2
import numpy as np

img = cv2.imread('test4.jpg')

cv2.namedWindow('bilateral blur', cv2.WINDOW_NORMAL)
cv2.resizeWindow('bilateral blur', 480, 640)

bilateralBlurImg = cv2.bilateralFilter(img, 25, 25 * 2, 25 / 2)

cv2.imshow('bilateral blur', bilateralBlurImg)

cv2.waitKey()

cv2.destroyAllWindows()