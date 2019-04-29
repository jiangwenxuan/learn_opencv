import cv2
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt

def predict():
	img = cv2.imread("number_test.jpg")
	pic_height, pic_width = img.shape[:2]

	img = cv2.GaussianBlur(img, (3, 3), 0)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	kernel = np.ones((20, 20), np.uint8)
	img_opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
	img_opening = cv2.addWeighted(img, 1, img_opening, -1, 0)
	
	ret, img_thresh = cv2.threshold(img_opening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	img_edge = cv2.Canny(img_thresh, 100, 200)

	kernel = np.ones((4, 4), np.uint8)
	img_edge1 = cv2.morphologyEx(img_edge, cv2.MORPH_CLOSE, kernel)
	img_edge2 = cv2.morphologyEx(img_edge1, cv2.MORPH_OPEN, kernel)

	plt.imshow(img)
	plt.show()
	# contours, hierarchy = cv2.findContours(img_edge2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	# contours = [cnt for cnt in contours if cv2.contourArea(cnt) < 1000]

	# print('len(contours)', len(contours))

	# test_contours = []
	# for cnt in contours:
	# 	rect = cv2.minAreaRect(cnt)
	# 	area_width, area_height = rect[1]
	# 	if area_width < area_height:
	# 		area_width, area_height = area_height, area_width
	# 	
predict()
