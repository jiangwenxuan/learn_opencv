from __future__ import print_function
import sys
import time
from random import randint
import cv2
import serial
import imutils
from imutils.video import FPS, VideoStream

# 英文注释部分是对代码的说明，为了方便使用，我又改成中文注释

class track():
    def __init__(self, com):
        self.trackerTypes = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT']
        self.trackerType = 'CSRT'
        self.bboxes = []
        self.colors = []
        self.ser = self.serialCreate(com)
        self.pixel = []
        self.shapeX = 0
        self.shapeY = 0
        self.speed = []

# change speed(hex) into speed(dec)
    def speedArea(self, hexSpeed):
        for i in hexSpeed:
            m = int(i, 16)
            self.speed.append(m) 

# make sure how to split the pixel, numArea is the num of the split area, theScale is the scale of turn and straight
# we use splitPixel in start_track()
    def splitPixel(self, numArea, theScale):
        currNum = (numArea - 1) * theScale + 1
        currPixel = int(self.shapeX / currNum)
        middle = int(numArea / 2)
        currTotal = 0
        for i in range(numArea - 1):
            if i != middle:
                currTotal = currTotal + currPixel * theScale
                self.pixel.append(currTotal)
            else:
                currTotal = currTotal + currPixel
                self.pixel.append(currTotal)
        self.pixel.append(self.shapeX)

# init serial port
# we use serialCreate in start_track()
    def serialCreate(self, com):
        timex = 5
        bps = 9600
        portx = com
        ser = serial.Serial(portx, bps, timeout = timex)
        return ser

# choose tracker
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
    def before_track(self, frame, multiTTracker):
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
        for i in contours:
            x, y, w, h = cv2.boundingRect(i)
            if w * h > 5:
                multiTTracker.add(self.createTrackerByName(self.trackerType), frame, (x, y, w, h))


# start track
    def startTrack(self, camera, numArea, theScale):
        cap = cv2.VideoCapture(camera)

        success, frame = cap.read()
        if not success:
            print("failed to read video")
            sys.exit(1)

        self.shapeX = frame.shape[1]
        self.shapeY = frame.shape[0]
        self.splitPixel(numArea, theScale)
        
        while True:
            ans = self.detailOfTrack(cap)
            if ans == 0:
                break

        cap.release()
        cv2.destroyAllWindows()
    
    def detailOfTrack(self, cap):
        self.bboxes.clear()
        self.colors.clear()
        mark = 0
        multiTracker = cv2.MultiTracker_create()
        maxX = 5
        maxY = 5
        maxW = 5
        maxH = 5

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                return 1

            if len(self.bboxes) != 0:
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
                        maxX = newbox[0]
                        maxY = newbox[1]
                        maxW = newbox[2]
                        maxH = newbox[3]
                    cv2.rectangle(frame, p1, p2, self.colors[i], 2, 1)
            
                if (maxX <= 5) or (maxY <= 5) or (maxX + maxW - 5 >= self.shapeX) or (maxY + maxH - 5 >= self.shapeY):
                    if mark > 5:
                        return 1
                    mark = mark + 1

# use serial port to control the ship  
                curr = 0
                for i in range(len(self.pixel)):
                    if offsetX <= self.pixel[i]:
                        curr = i
                        break
                m = bytes([self.speed[curr]])
                self.ser.write(m)

            cv2.imshow('multiTracker', frame)

            k = cv2.waitKey(1) & 0xFF

            if k == ord('q'):
                return 0
            
            if k == ord('t'):
                return 1

# 鼠标框定代码，改用颜色分割则注释此段代码
            if k == ord('s'):
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
                    multiTracker.add(self.createTrackerByName(self.trackerType), frame, bbox)

# 颜色分割自动框定目标代码，需要的话取消注释，还未完成
            # if k == ord('s'):
            #     self.before_track(frame, multiTracker)


# 以下部分是参数设置部分，可以修改

# 速度可以自己增加
speed = ['0x46', '0x56', '0x66', '0x65', '0x64']

# 可以在这里修改占用的串口
track1 = track("COM1")
# 把speed转化10进制
track1.speedArea(speed)

# 第一个参数是摄像头编号，可能是0, 1, 2......n
# 第二个参数是屏幕一共要分几个区，不同的区是不同的电机转速，与speed[]对应
# 第三个参数是一个转向分区和中间的直行分区的像素宽度的比值
track1.startTrack(0, 5, 3)

# 用鼠标框定追踪目标指南
# PS：在摄像头打开后，按‘s’是暂停这帧，框定目标后按回车，再按任意键，可以框定第二个目标
# PS：框定结束后按‘q’，开始追踪
# PS：按‘t’，退出此次追踪，开始下一次追踪
# PS：按‘q’退出程序