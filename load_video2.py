import numpy as np
import cv2

cap = cv2.VideoCapture('test.avi')
index = 0
imgname = 0

while True:
	index = index + 1
	ret, img = cap.read()
	cv2.imshow('camera', img)
	if index == 10:
		imgname = imgname + 1
		if imgname >= 50:
			imgname = 0

		fname = str(imgname) + '.jpg'
		cv2.imwrite(fname, img)
		print(fname + ' saved')
		index = 0

	if cv2.waitKey(50) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
