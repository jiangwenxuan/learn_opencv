import numpy as np
import matplotlib.pyplot as plt
import cv2
from matplotlib.colors import hsv_to_rgb
from matplotlib import cm
from matplotlib import colors

flags = [i for i  in dir(cv2) if i.startswith('COLOR_')]

print(len(flags))
print(flags[40])

nemo = cv2.imread('nemo0.jpg')
nemo = cv2.cvtColor(nemo, cv2.COLOR_BGR2RGB)
hsv_nemo = cv2.cvtColor(nemo, cv2.COLOR_RGB2HSV)

light_orange = (1, 190, 200)
dark_orange = (18, 255, 255)

lo_square = np.full((10, 10, 3), light_orange, dtype=np.uint8) / 255.0
do_square = np.full((10, 10, 3), dark_orange, dtype=np.uint8) / 255.0

"""
plt.subplot(1, 2, 1)
plt.imshow(hsv_to_rgb(do_square))
plt.subplot(1, 2, 2)
plt.imshow(hsv_to_rgb(lo_square))
plt.show()
"""
mask = cv2.inRange(hsv_nemo, light_orange, dark_orange)

result = cv2.bitwise_and(nemo, nemo, mask=mask)
"""
plt.subplot(1, 2, 1)
plt.imshow(mask, cmap='gray')
plt.subplot(1, 2, 2)
plt.imshow(result)
plt.show()
"""
light_white = (0, 0, 200)
dark_white = (145, 60, 255)

mask_white = cv2.inRange(hsv_nemo, light_white, dark_white)
result_white = cv2.bitwise_and(nemo, nemo, mask=mask_white)

final_mask = mask + mask_white

final_mask = cv2.bitwise_and(nemo, nemo, mask=final_mask)

blur = cv2.GaussianBlur(final_mask, (7, 7), 0)
plt.imshow(nemo)
plt.show()