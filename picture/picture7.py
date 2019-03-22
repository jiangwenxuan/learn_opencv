import cv2
import numpy as np

def threshBar(x):
    pass

img = cv2.imread('test2.jpg')
grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.namedWindow('thresh window')
cv2.namedWindow('test window')
cv2.imshow('test window', grayImg)

cv2.createTrackbar('thresh', 'thresh window', 0, 200, threshBar)

while True:
	threshValue = cv2.getTrackbarPos('thresh', 'threash window')
	retval, threshImg = cv2.threshold(grayImg, threshValue, 255, cv2.THRESH_BINARY)
	cv2.imshow('thresh window', threshImg)
	if cv2.waitKey(1) & 0xFF is ord('q'):
		break

cv2.destroyAllWindows()
