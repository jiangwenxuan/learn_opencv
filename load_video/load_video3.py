import numpy as np
import cv2

cap = cv2.VideoCapture('test.mp4')
# 定义fourecc代码
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

all_images = []

i = 0

while cap.isOpened():
    ret, frame = cap.read()
    i = i + 1
    if ret is True:
        if i is 3:
            i = 0
            blurImg = cv2.GaussianBlur(frame, (9, 9), 0)
            frameGray = cv2.cvtColor(blurImg, cv2.COLOR_BGR2GRAY)
            ret, threshFrame = cv2.threshold(frameGray, 122, 255, cv2.THRESH_BINARY)
            cannyImg = cv2.Canny(threshFrame, 50, 130)
# some deals
            cannyImg_inv = cv2.bitwise_not(cannyImg)
            cannyImg_mask1 = cv2.cvtColor(cannyImg_inv, cv2.COLOR_GRAY2BGR)
            cannySrcImg = cv2.bitwise_and(frame, cannyImg_mask1)
            cannyImg_mask2 = cv2.bitwise_not(cannyImg_mask1)
            cannyImg_mask2[:, :, [0, 1]] = 0
            cannyImg_target = cv2.add(cannySrcImg, cannyImg_mask2)

            all_images.append(cannyImg_target)
            cv2.imshow('camera', cannyImg_target)
            if cv2.waitKey(1) & 0xFF is ord('q'):
                break
    else:
        break

sample_img = all_images[0]
size = (sample_img.shape[1], sample_img.shape[0])
# 创建VideoWriter对象
out = cv2.VideoWriter('output5.avi', fourcc, 20.0, size)

for img in all_images:
    out.write(img)

cap.release()
out.release()
cv2.destroyAllWindows()
