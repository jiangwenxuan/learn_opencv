import cv2
import numpy as np

img = cv2.imread('test5.jpg')

blurImg = cv2.GaussianBlur(img, (9, 9), 0)

cannyImg = cv2.Canny(blurImg, 50, 130)

cv2.namedWindow('canny')
cv2.namedWindow('blur')
cv2.imshow('canny', cannyImg)
cv2.imshow('blur', blurImg)

cv2.waitKey()
cv2.destroyAllWindows()