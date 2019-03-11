import numpy as np
import cv2

'''
pix_bgr = img[100, 100]
print(pix_bgr)
pix_g = img[100, 100, 1]
print(pix_g)
img[100, 100] = [122, 122, 122]
'''

img = cv2.imread('test1.jpg', 1)

b, g, r = cv2.split(img)

cv2.namedWindow('source image')
cv2.namedWindow('blue channel')
cv2.namedWindow('green channel')
cv2.namedWindow('red channel')
cv2.imshow('source image', img)
cv2.imshow('blue channel', b)
cv2.imshow('green channel', g)
cv2.imshow('red channel', r)

cv2.namedWindow('test')
zeros = np.zeros(img.shape[:2], np.uint8)
test = cv2.imshow('test', cv2.merge([b, zeros, zeros]))

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv)
cv2.namedWindow('hsv')
cv2.namedWindow('h')
cv2.namedWindow('s')
cv2.namedWindow('v')
cv2.imshow('hsv', hsv)
cv2.imshow('h', h)
cv2.imshow('s', s)
cv2.imshow('v', v)

cv2.waitKey(0)
cv2.destroyAllWindows()
