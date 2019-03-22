import cv2
import numpy as np

img = cv2.imread('test7.jpg')

grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, binImg = cv2.threshold(grayImg, 100, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(binImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

cv2.drawContours(img, contours, 1, (0, 200, 0), 2)
cv2.imshow('contours image', img)

print(contours[1].shape)
cv2.waitKey()
cv2.destroyAllWindows()
