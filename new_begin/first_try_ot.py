import argparse
import sys
import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
from imutils.video import FPS, VideoStream


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', help = 'path to input file')
    args = vars(parser.parse_args())

    if not args.get('video', False):
        print('[info] starting video stream...')
        track('false')

# default tracker is kcf, you can change tracker in entity.Entity._init_tracker()
    else:
        track(args['video'])

def track(video):
    camera = cv2.VideoCapture(video)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('output1.avi', fourcc, 25.0, (1920, 1080))
    tracker = cv2.TrackerKCF_create()
    i = 0
    
    while True:
        res, frame = camera.read()

        if not res:
            break

# deal the frame to find the edge of our object
        if i == 0:
            test = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            hsv_test = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            light_orange = (80, 160, 150)
            dark_orange = (120, 220, 210)
            mask = cv2.inRange(hsv_test, light_orange, dark_orange)
            result = cv2.bitwise_and(test, test, mask = mask)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
            result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
            gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
            _, gray = cv2.threshold(gray, 100, 1, cv2.THRESH_BINARY)
            contours, hier = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            x, y, w, h = cv2.boundingRect(contours[0])
            bbox = (x, y, w, h)
#            bbox = cv2.selectROI(frame, False)
            tracker.init(frame, bbox)
            i = i + 1
            
        (success, box) = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow('track', frame)
        out.write(frame)
        if cv2.waitKey(30) & 0xFF == 'q':
            break
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
