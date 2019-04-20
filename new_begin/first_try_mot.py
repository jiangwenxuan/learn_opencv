from __future__ import print_function
import sys
import time
from random import randint
import cv2
# import imutils
# from imutils.video import FPS, VideoStream

trackerTypes = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT']

def createTrackerByName(trackerType):
    if trackerType == trackerTypes[0]:
        tracker = cv2.TrackerBoosting_create()
    elif trackerType == trackerTypes[1]:
        tracker = cv2.TrackerMIL_create()
    elif trackerType == trackerTypes[2]:
        tracker = cv2.TrackerKCF_create()
    elif trackerType == trackerTypes[3]:
        tracker = cv2.TrackerTLD_create()
    elif trackerType == trackerTypes[4]:
        tracker = cv2.TrackerMedianFlow_create()
    elif trackerType == trackerTypes[5]:
        tracker = cv2.TrackerMOSSE_create()
    elif trackerType == trackerTypes[6]:
        tracker = cv2.TrackerCSRT_create()
    else:
        tracker = None
        print("incorrect tracker name")
        print("available trackers are:")
        for t in trackerTypes:
            print(t)

    return tracker

if __name__ == '__main__':
    
    trackerType = 'CSRT'
    cap = cv2.VideoCapture(1)
    
    success, frame = cap.read()
    if not success:
        print("failed to read video")
        sys.exit(1)
    
    bboxes = []
    colors = []

    multiTracker = cv2.MultiTracker_create()

    while True:
        bbox = cv2.selectROI('multiTracker', frame)
        bboxes.append(bbox)
        colors.append((randint(64, 255), randint(64, 255), randint(64, 255)))
        print("press q to quit selecting boxes and start tracking")
        print("press any other key to select next object")
        k = cv2.waitKey(0) & 0xFF
        if k == ord('q'):
            break

    for bbox in bboxes:
        multiTracker.add(createTrackerByName(trackerType), frame, bbox)
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        success, boxes = multiTracker.update(frame)
        for i, newbox in enumerate(boxes):
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

        cv2.imshow('multiTracker', frame)

        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
