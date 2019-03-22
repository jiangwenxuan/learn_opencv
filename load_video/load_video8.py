import numpy as np
import cv2

cap = cv2.VideoCapture('test.avi')

fourcc = cv2.VideoWriter_fourcc(*'MJPG')

all_images = []

i = 0

while cap.isOpened():
	ret, frame = cap.read()
	i = i + 1
	if ret is True:
		if i is 3:
			i = 0
			grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			_, binImg = cv2.threshold(grayImg, 100, 255, cv2.THRESH_BINARY)
			contours, hierarchy = cv2.findContours(binImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
			cv2.drawContours(frame, contours, 1, (0, 200, 0), 2)
			x, y, w, h = cv2.boundingRect(contours[1])
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 200), 2)
			all_images.append(frame)
			cv2.imshow('movie', frame)
			cv2.imshow('test1', binImg)
			if cv2.waitKey(15) & 0xFF is ord('q'):
				break
	else:
		break

sample_img_shape = all_images[0].shape
size = (sample_img_shape[1], sample_img_shape[0])

out = cv2.VideoWriter('output6.avi', fourcc, 20.0, size)

for img in all_images:
	out.write(img)

cap.release()
cap.release()
cv2.destroyAllWindows()
