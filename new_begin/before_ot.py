import numpy as np
import cv2
import matplotlib.pyplot as plt

cap = cv2.VideoCapture('try.avi')

# fourcc = cv2.VideoWriter_fourcc(*'MJPG')

i = 0

while cap.isOpened():
    ret, frame = cap.read()
    i = i + 1
    if ret is True:
        if i is 3:
            i = 0
            test = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            hsv_test = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            light_orange = (80, 160, 150)
            dark_orange = (120, 220, 210)
            mask = cv2.inRange(hsv_test, light_orange, dark_orange)
            result = cv2.bitwise_and(test, test, mask = mask)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
            result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
            gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
            _, gray = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
            contours, hier = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            x, y, w, h = cv2.boundingRect(contours[0])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 200, 200), 2)
            cv2.imshow('movie', frame)
            if cv2.waitKey(15) & 0xFF is ord('q'):
                break
    else:
        break

# sample_img_shape = all_images[0].shape
# size = (sample_img_shape[1], sample_img_shape[0])

# out = cv2.VideoWriter('output6.avi', fourcc, 20.0, size)

# for img in all_images:
#     out.write(img)

cap.release()
cv2.destroyAllWindows()
