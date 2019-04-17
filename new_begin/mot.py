import argparse
import sys
import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
from imutils.video import FPS, VideoStream

from entity import Entity


def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('--video', help = 'path to input file')
    parser.add_argument('--iou', default = 0.2, help = 'threshold for tracking')
    args = vars(parser.parse_args())

    if not args.get('video', False):
        print('[info] starting video stream...')
        track('false', args['iou'])

# default tracker is kcf, you can change tracker in entity.Entity._init_tracker()
    else:
        track(args['video'], args['iou'])


def overlap(box1, box2):
# check the overlap of two boxes
    endx = max(box1[0] + box1[2], box2[0] + box[2])
    startx = min(box1[0], box2[0])
    width = box1[2] + box2[2] - (endx - startx)

    endy = max(box1[1] + box1[3], box2[1] + box2[3])
    starty = min(box1[1], box2[1])
    height = box1[3] + box2[3] - (endy - starty)

    if (width <= 0 or height <= 0):
        return 0
    else:
        area = width * height
        area1 = box1[2] * box1[3]
        area2 = box2[2] * box2[3]
        ratio = area / (area1 + area2 - area)
        return ratio


def track(video, iou):
    if video == 'false':
        vs = VideoStream(src = 0).start()
        time.sleep(1.0)
    else:
        camera = cv2.VideoCapture(video)
    
    res, frame = camera.read()
    y_size = frame.shape[0]
    x_size = frame.shape[1]

    counter = 0

    track_list = []
    while True:
        res, frame = camera.read()

        if not res:
            break

# deal the frame to find the edge of our object
        test = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hsv_test = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        light_orange = (17, 150, 150)
        dark_orange = (22, 210, 210)
        mask = cv2.inRange(hsv_test, light_orange, dark_orange)
        result = cv2.bitwise_and(test, test, mask = mask)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
        result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
        gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
        _, gray = cv2.threshold(gray, 100, 1, cv2.THRESH_BINARY)
        contours, hier = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            e = Entity(counter, (x, y, w, h), frame)

            if track_list:
                count = 0
                num = len(track_list)
                for p in track_list:
                    if (overlap((x, y, w, h), p.windows)) < iou:
                        count = count + 1
                if count == num:
                    track_list.append(e)
            else:
                track_list.append(e)
            counter = counter + 1
        
        if track_list:
            tlist = copy.copy(track_list)
            for e in tlist:
                x, y = e.center
                if 10 < x < x_size - 10 and 10 < y < y_size - 10:
                    e.update(frame)
                else:
                    track_list.remove(e)
        cv2.imshow('detection', frame)
        if cv2.waitKey(30) &0xFF == 'q':
            break
    camera.release()

if __name__ == '__main__':
    main(sys.argv)
