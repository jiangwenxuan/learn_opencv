import cv2
import numpy as np

img1 = cv2.imread('test2.jpg')
img2 = cv2.imread('test3.jpg')

rows1, cols1, channels1 = img1.shape
rows2, cols2, channels2 = img2.shape
roi = img1[rows1-rows2:rows1, cols1-cols2:cols1]

img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 170, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)
cv2.namedWindow('mask_inv')
cv2.imshow('mask_inv', mask_inv)

img1_bg = cv2.bitwise_and(roi, roi, mask = mask)

img2_fg = cv2.bitwise_and(img2, img2, mask = mask_inv)

dst = cv2.add(img1_bg, img2_fg)
cv2.imwrite('merge.jpg', dst)
roi[:] = dst

cv2.imshow('res', img1)
cv2.waitKey(0)
cv2.destroyAllWindows()
