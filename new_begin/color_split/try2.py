import numpy as np
import cv2
from matplotlib.colors import hsv_to_rgb
from matplotlib import colors

cap = cv2.VideoCapture('../try.avi')
i = 0
while cap.isOpened():
	if i == 0:
		ret, frame = cap.read()
		i = i + 1
		if ret is True:
			cv2.imwrite('judge2.jpg', frame)
	else:
		break
cv2.destroyAllWindows()