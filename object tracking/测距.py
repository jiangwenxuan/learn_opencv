from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import argparse
import imutils
import numpy as np
import cv2

cap = cv2.VideoCapture(0)

hog = cv2.HOGDescriptor()

hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

while 1:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width = min(400, frame.shape[1]))
    (rects, weights) = hog.detectMultiScale(frame, winDtride=(4, 4), \
        padding=(8, 8), scale=1.05)
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])

    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    for (xA, yA, xB, yB) in pick:
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)

    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()