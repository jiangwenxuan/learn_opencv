import cv2
import numpy as np

img1 = cv2.imread('test2.jpg')
img2 = cv2.imread('test3.jpg')

img1Shape = img2.shape
roi = img1[0:img1Shape[0], 0:img1Shape[1]]

img3 = cv2.addWeighted(roi, 0.5, img2, 0.5, 0)

cv2.namedWindow('img1')
cv2.namedWindow('img2')
cv2.namedWindow('img3')
cv2.imshow('img1', img1)
cv2.imshow('img2', img2)
cv2.imshow('img3', img3)

cv2.imwrite('addTest2Test3.jpg', img3)

cv2.waitKey(0)
cv2.destroyAllWindows()
