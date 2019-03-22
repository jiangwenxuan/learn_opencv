import cv2
import numpy as np

def drawfindLines_hough(img, lines):
	for i in lines:
		for rho, theta in i:
			a = np.cos(theta)
			b = np.sin(theta)
			x0 = a * rho
			y0 = b * rho
			x1 = int(x0 + 1000 * (-b))
			y1 = int(y0 + 1000 * (a))
			x2 = int(x0 - 1000 * (-b))
			y2 = int(x0 - 1000 * (a))
			cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)

img = cv2.imread('test6.jpg')
blurImg = cv2.GaussianBlur(img, (9, 9), 0)
gray = cv2.cvtColor(blurImg, cv2.COLOR_BGR2GRAY)
ret, threshFrame = cv2.threshold(gray, 122, 255, cv2.THRESH_BINARY)
edges = cv2.Canny(threshFrame, 50, 150, apertureSize = 3)

lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
drawfindLines_hough(img, lines)

cv2.imshow('edges', edges)
cv2.imshow('line', img)
cv2.waitKey()
cv2.destroyAllWindows()
