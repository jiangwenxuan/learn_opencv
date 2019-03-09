import cv2
import numpy as np
from matplotlib import pyplot as plt

""" use opencv to open a image """
img = cv2.imread('watch.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


""" use matplotlib to open a image 

img = cv2.imread('watch.jpg', cv2.IMREAD_GRAYSCALE)

plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])
plt.plot([200, 300, 400], [100, 200, 300], 'c', linewidth = 5)
plt.show()
"""