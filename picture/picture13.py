import cv2
import numpy as np

img = cv2.imread('test1.jpg')

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
dilateImg = cv2.dilate(img, kernel)
erodeImg = cv2.erode(img, kernel)

cv2.imshow('srcImg', img)
cv2.imshow('dilateImg', dilateImg)
cv2.imshow('erodeImg', erodeImg)

cv2.waitKey()
cv2.destroyAllWindows()