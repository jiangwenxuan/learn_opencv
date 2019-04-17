import numpy as np
import matplotlib.pyplot as plt
import cv2
#from imutils.video import VideoStream
#from imutils.video import FPS
import time
import argparse
import sys

from entity import Entity

def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--video', type = str, \
        help = 'path to input file')
    parser.add_argument('-t', '--tracker', type = str, \
        default = 'kcf', help = 'OpenCV object tracker type')
    args = vars(parser.parse_args())

    (major, minor) = cv2.__version__.split('.')[:2]

    if int(major) == 3 and int(minor) < 3:
        tracker = cv2.Tracker_create(args['tracker'].upper())
    else:
        OPENCV_OBJECT_TRACKERS = {
            "csrt": cv2.TrackerCSRT_create,
            "kcf": cv2.TrackerKCF_create,
            "boosting": cv2.TrackerBoosting_create,
            "mil": cv2.TrackerMIL_create,
            "tld": cv2.TrackerTLD_create,
            "medianflow": cv2.TrackerMedianFlow_create,
            "mosse": cv2.TrackerMOSSE_create
        }
        tracker = OPENCV_OBJECT_TRACKERS[args['tracker']]()

    if not args.get('video', False):
        print('[info] starting video stream...')
        vs = VideoStream(src = 0).start()
        time.sleep(1.0)
    else:
        vs = cv2.VideoCapture(args['video'])

    track(tracker, args['video'])

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

def track(tracker, video):
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

            img = frame[y : y + h, x : x + w, :]
            rimg = cv2.resize(img, (64, 64), interpolation = cv2.INTER_CUBIC)
            image_data = np.array(rimg, dtype = 'float32')
            image_data /= 255
            roi = np.expand_dims(image_data, axis = 0)
# some judge function

            e = Entity(counter, (x, y, w, h), frame)

            if track_list:
                count = 0
                num = len(track_list)
                for p in track_lisk:
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
        frames += 1
        cv2.imshow('detection', frame)
        if cv2.waitKey(30) &0xFF == 'q':
            break
    camera.release()

if __name__ == '__main__':
    main(sys.argv)