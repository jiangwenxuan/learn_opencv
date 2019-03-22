import cv2
import numpy as np

img = cv2.imread('test1.jpg')

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
openImg = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
closeImg = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
gradImg = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

cv2.imshow('openImg', openImg)
cv2.imshow('closeImg', closeImg)
cv2.imshow('gradImg', gradImg)

cv2.waitKey()
cv2.destroyAllWindows()