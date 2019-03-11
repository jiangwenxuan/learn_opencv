import numpy as np
import cv2

cap = cv2.VideoCapture('test.mp4')

while True:
	if cap.isOpened():
	    ret, frame = cap.read()
	    cv2.imshow('camara', frame)
	    if cv2.waitKey(100) & 0xFF is ord('q'):
		    break

cv2.destroyAllWindows()