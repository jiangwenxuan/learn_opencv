import cv2
import numpy as np

def threshBar(x):
	pass

img = cv2.imread('test3.jpg')
grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
shape = grayImg.shape

cv2.namedWindow('thresh window', cv2.WINDOW_NORMAL)
cv2.namedWindow('adaptiveThresh window', cv2.WINDOW_NORMAL)
cv2.namedWindow('bgr thresh window', cv2.WINDOW_NORMAL)

cv2.resizeWindow('thresh window', shape[1], shape[0])
cv2.resizeWindow('adaptiveThresh window', shape[1], shape[0])
cv2.resizeWindow('bgr thresh window', shape[1], shape[0])

ret, threshImg = cv2.threshold(grayImg, 122, 255, cv2.THRESH_BINARY)
ret, bgrThreshImg = cv2.threshold(img, 122, 255, cv2.THRESH_BINARY)
adaptiveThreshImg = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 49, 0)
cv2.imshow('adaptiveThresh window', adaptiveThreshImg)
cv2.imshow('thresh window', threshImg)
cv2.imshow('bgr thresh window', bgrThreshImg)

cv2.waitKey()
cv2.destroyAllWindows()
