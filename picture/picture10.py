import cv2
import numpy as np

def medianBlurTrackbar(x):
	pass

img = cv2.imread('test4.jpg')

cv2.namedWindow('median blur', cv2.WINDOW_NORMAL)
cv2.resizeWindow('median blur', 480, 640)

cv2.createTrackbar('ksize', 'median blur', 1, 30, medianBlurTrackbar)

while True:
	medianKsize = cv2.getTrackbarPos('ksize', 'median blur')

	if medianKsize % 2 is 0:
		medianKsize = medianKsize + 1

	meidanBlurImg = cv2.medianBlur(img, medianKsize)

	cv2.imshow('median blur', meidanBlurImg)

	if cv2.waitKey(1) & 0xFF is ord('q'):
		break

cv2.destroyAllWindows()