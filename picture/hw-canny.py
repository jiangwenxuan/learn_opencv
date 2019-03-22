import cv2
import numpy as np

img = cv2.imread('test5.jpg')

blurImg = cv2.GaussianBlur(img, (9, 9), 0)

cannyImg = cv2.Canny(blurImg, 50, 130)

cannyImg_inv = cv2.bitwise_not(cannyImg)

cannyImg_mask1 = cv2.cvtColor(cannyImg_inv, cv2.COLOR_GRAY2BGR)

cannySrcImg = cv2.bitwise_and(img, cannyImg_mask1)

cannyImg_mask2 = cv2.bitwise_not(cannyImg_mask1)

cannyImg_mask2[:, :, [0, 1]] = 0

cannyImg_target = cv2.add(cannySrcImg, cannyImg_mask2)

cv2.namedWindow('cannyImg')
cv2.namedWindow('cannyImg_inv')
cv2.namedWindow('cannyImg_mask1')
cv2.namedWindow('cannySrcImg')
cv2.namedWindow('cannyImg_mask2')
cv2.namedWindow('target')
cv2.imshow('cannyImg', cannyImg)
cv2.imshow('cannyImg_inv', cannyImg_inv)
cv2.imshow('cannyImg_mask1', cannyImg_mask1)
cv2.imshow('cannySrcImg', cannySrcImg)
cv2.imshow('cannyImg_mask2', cannyImg_mask2)
cv2.imshow('target', cannyImg_target)

cv2.waitKey()
cv2.destroyAllWindows()