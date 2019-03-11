import cv2
import numpy as np

a = np.zeros((500, 500), np.uint8)
b = np.zeros((500, 500), np.uint8)

print(a)
print(b)

c = a + b

d = cv2.add(a, b)

cv2.namedWindow('b')
cv2.imshow('b', b)

b = b + 120

cv2.namedWindow('b + 120')
cv2.imshow('b + 120', b)

cv2.namedWindow('add')
cv2.imshow('add', d)

print(c.all() == d.all())

cv2.waitKey()
cv2.destroyAllWindows()