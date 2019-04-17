import numpy as np
import matplotlib.pyplot as plt
import cv2
from matplotlib.colors import hsv_to_rgb
from matplotlib import cm
from matplotlib import colors

test = cv2.imread('judge.jpg')
test = cv2.cvtColor(test, cv2.COLOR_BGR2RGB)
hsv_test = cv2.cvtColor(test, cv2.COLOR_RGB2HSV)
"""
plt.subplot(1, 2, 1)
plt.imshow(test)
plt.subplot(1, 2, 2)
plt.imshow(hsv_test)
plt.show()
"""
light_orange = (17, 150, 150)
dark_orange = (22, 210, 210)

mask = cv2.inRange(hsv_test, light_orange, dark_orange)
result = cv2.bitwise_and(test, test, mask = mask)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
#blur = cv2.GaussianBlur(result, (7, 7), 0)
gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
_, gray = cv2.threshold(gray, 100, 1, cv2.THRESH_BINARY)
contours, hier = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#plt.subplot(1, 2, 1)
#plt.imshow(gray)
#test = cv2.cvtColor(test, cv2.COLOR_RGB2BGR)
#cv2.drawContours(test, contours, 1, (0, 200, 0), 2)
#plt.subplot(1, 2, 2)
print(test.shape)
x, y, w, h = cv2.boundingRect(contours[0])
cv2.rectangle(test, (x, y), (x+w, y+h), (0, 0, 200), 2)
plt.imshow(test)
plt.show()