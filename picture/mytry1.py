import cv2
import numpy as np

img = cv2.imread('test5.jpg')

blurImg = cv2.GaussianBlur(img, (9, 9), 0)
grayImg = cv2.cvtColor(blurImg, cv2.COLOR_BGR2GRAY)
ret, newImg = cv2.threshold(grayImg, 122, 255, cv2.THRESH_BINARY)
cannyImg = cv2.Canny(newImg, 50, 130)

cv2.namedWindow('canny')
cv2.namedWindow('blur')
cv2.namedWindow('thresh')
cv2.namedWindow('img')
cv2.imshow('canny', cannyImg)
cv2.imshow('blur', blurImg)
cv2.imshow('thresh', newImg)
cv2.imshow('img', img)

cv2.waitKey()
cv2.destroyAllWindows()
