import cv2
import numpy as np

def threshBar(x):
	pass

cap = cv2.VideoCapture('test.avi')
i = 0

cv2.namedWindow('camera')
cv2.namedWindow('thresh window')

while True:
	i = i + 1
	ret, img = cap.read()
	if ret is True:
		ret, img = cap.read()
		grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		threshImg = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 49, 0)
		cv2.imshow('camera', img)
		if i is 5:
			i = 0
			cv2.imshow('thresh window', threshImg)
		if cv2.waitKey(25) & 0xFF is ord('q'):
			break
	else:
		break

cv2.destroyAllWindows()
