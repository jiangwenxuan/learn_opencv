from __future__ import print_function
import sys
import time
from random import randint
import cv2
import serial
# import imutils
# from imutils.video import FPS, VideoStream

class track():
    def __init__(self):
        self.trackerTypes = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT']
        self.bboxes = []
        self.colors = []
        self.ser = self.serialCreate()

    def serialCreate(self):
        timex = 5
        bps = 115200
        portx = "COM1"
        ser = serial.Serial(portx, bps, timeout = timex)
        return ser

# choose out tracker
    def createTrackerByName(self, trackerType):
        if trackerType == self.trackerTypes[0]:
            tracker = cv2.TrackerBoosting_create()
        elif trackerType == self.trackerTypes[1]:
            tracker = cv2.TrackerMIL_create()
        elif trackerType == self.trackerTypes[2]:
            tracker = cv2.TrackerKCF_create()
        elif trackerType == self.trackerTypes[3]:
            tracker = cv2.TrackerTLD_create()
        elif trackerType == self.trackerTypes[4]:
            tracker = cv2.TrackerMedianFlow_create()
        elif trackerType == self.trackerTypes[5]:
            tracker = cv2.TrackerMOSSE_create()
        elif trackerType == self.trackerTypes[6]:
            tracker = cv2.TrackerCSRT_create()
        else:
            tracker = None
            print("incorrect tracker name")
            print("available trackers are:")
            for t in trackerTypes:
                print(t)
        return tracker

# use color segmentation to find out object
    def before_track(self, frame):
        test = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hsv_test = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        # color segmentation
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


    def start_track(self):
        
        trackerType = 'CSRT'
        cap = cv2.VideoCapture(0)
        
        success, frame = cap.read()
        shapeX = frame.shape[1]
        if not success:
            print("failed to read video")
            sys.exit(1)

        multiTracker = cv2.MultiTracker_create()

        while True:
            bbox = cv2.selectROI('multiTracker', frame)
            self.bboxes.append(bbox)
            self.colors.append((randint(64, 255), randint(64, 255), randint(64, 255)))
            print("press q to quit selecting boxes and start tracking")
            print("press any other key to select next object")
            k = cv2.waitKey(0) & 0xFF
            if k == ord('q'):
                break

        for bbox in self.bboxes:
            multiTracker.add(self.createTrackerByName(trackerType), frame, bbox)
        
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
            success, boxes = multiTracker.update(frame)
            maxObject = 0
            offsetX = 0
            for i, newbox in enumerate(boxes):
                p1 = (int(newbox[0]), int(newbox[1]))
                p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
                currentArea = newbox[2] * newbox[3]
                if maxObject < currentArea:
                    maxObject = currentArea
                    offsetX = int(newbox[0] + (newbox[2] / 2))
                cv2.rectangle(frame, p1, p2, self.colors[i], 2, 1)
                
# use serial port send the nearest object's x's position
            offsetX = ((offsetX / shapeX) * 255) + 0.5
            offsetX = int(offsetX)
# dec to byte
            m = bytes([offsetX])

            self.ser.write(m)
            
            cv2.imshow('multiTracker', frame)

            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

track1 = track()
track1.start_track()
