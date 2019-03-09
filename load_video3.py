import numpy as np
import cv2

cap = cv2.VideoCapture('D:\cs\learn_opencv\resource\test.avi')
# 定义fourecc代码
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

all_images = []
while cap.isOpened():
    ret, frame = cap.read()
    if ret is True:
        all_images.append(frame)
        cv2.imshow('camera', frame)
        if cv2.waitKey(1) & 0xFF is ord('q'):
            break
    else:
        break

sample_img = all_images[0]
size = (sample_img.shape[1], sample_img.shape[0])
# 创建VideoWriter对象
out = cv2.VideoWriter('output.avi', fourcc, 20.0, size)

for img in all_images:
    out.write(img)

cap.release()
out.release()
cv2.destroyAllWindows()
