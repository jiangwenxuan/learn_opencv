import numpy as np
import cv2

cap = cv2.VideoCapture('test.avi')
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

all_images1 = []
all_images2 = []

cv2.namedWindow('1')
cv2.namedWindow('2')

i = 0

while cap.isOpened():
    ret, frame = cap.read()
    i = i + 1
    if ret is True:
        if i is 3:
            i = 0
            newFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame1 = cv2.adaptiveThreshold(newFrame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 49, 0)
            retu, frame2 = cv2.threshold(newFrame, 122, 255, cv2.THRESH_BINARY)
            all_images1.append(frame1)
            all_images2.append(frame2)
            cv2.imshow('1', frame1)
            cv2.imshow('2', frame2)
            if cv2.waitKey(1) & 0xFF is ord('q'):
                break
    else:
        break

shape1 = all_images1[0].shape
shape2 = all_images2[0].shape
size1 = (shape1[1], shape1[0])
size2 = (shape2[1], shape2[0])

out1 = cv2.VideoWriter('outputNew1.avi', fourcc, 20.0, size1, False)
out2 = cv2.VideoWriter('outputNew2.avi', fourcc, 20.0, size2, False)

for img in all_images1:
    out1.write(img)
for img in all_images2:
    out2.write(img)

cap.release()
out1.release()
out2.release()
cv2.destroyAllWindows()
