import cv2
import numpy as np

img = cv2.imread('test1.jpg', 1)

b, g, r = cv2.split(img)

cv2.namedWindow('source image')
cv2.namedWindow('new red channel')
cv2.namedWindow('new image')

cv2.imshow('source image', img)

rShape = r.shape

roi = r[(int)(0.5 * rShape[0]): , (int)(0.5 * rShape[1]): ]
roi = 255
r[(int)(0.5 * rShape[0]): , (int)(0.5 * rShape[1]): ] = roi

cv2.imshow('new red channel', r)
newImage = cv2.merge((b, g, r))
cv2.imshow('new image', newImage)

cv2.waitKey(0)
cv2.destroyAllWindows()
