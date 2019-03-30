import cv2
import numpy as np

img = cv2.imread('test1.jpg')

grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binImg = cv2.threshold(grayImg, 100, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(binImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

cv2.drawContours(img, contours, 1, (0, 200, 0), 2)
x, y, w, h = cv2.boundingRect(contours[1])
cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 200), 2)
cv2.imshow('coutours image', img)
cv2.imshow('test', binImg)

cv2.waitKey()
cv2.destroyAllWindows()