import cv2
import numpy as np

def blurTrackbar(x):
	pass

def GaussianBlurTrackbar(x):
	pass

img = cv2.imread('test4.jpg')

cv2.namedWindow('blur', cv2.WINDOW_NORMAL)
cv2.resizeWindow('blur', 480, 640)
cv2.namedWindow('gaussian blur', cv2.WINDOW_NORMAL)
cv2.resizeWindow('gaussian blur', 480, 640)

cv2.createTrackbar('ksize', 'blur', 1, 30, blurTrackbar)
cv2.createTrackbar('ksize', 'gaussian blur', 1, 30, GaussianBlurTrackbar)

while True:
	blurKsize = cv2.getTrackbarPos('ksize', 'blur')
	gaussianKsize = cv2.getTrackbarPos('ksize', 'gaussian blur')

	blurImg = cv2.blur(img, (blurKsize, blurKsize))

	if gaussianKsize % 2 is 0:
		gaussianKsize = gaussianKsize + 1

	gauBlurImg = cv2.GaussianBlur(img, (gaussianKsize, gaussianKsize), 0, None, 0)

	cv2.imshow('blur', blurImg)
	cv2.imshow('gaussian blur', gauBlurImg)

	if cv2.waitKey(1) & 0xFF is ord('q'):
		break

cv2.destroyAllWindows()
