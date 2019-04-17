from __future__ import print_function
import sys
import cv2
from random import randint

trackerTypes = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'MOSSE', 'CSRT']

def createTrackerByName(trackerType):
	if trackerType == trackerTypes[0]:
		tracker = cv2.TrackerBoosting_create()
	elif trackerType == trackerTypes[1]:
		tracker = cv2.TrackerMIL_create()
	elif trackerType == trackerTypes[2]:
		tracker = cv2.TrackerKCF_create():
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
		print('incorrect tracker name')
		print("available trackers are: ")
		for t in trackerTypes:
			print(t)
	return tracker

videoPath = "video/run.mp4"

cap = cv2.VideoCapture(videoPath)

success, frame = cap.read()

if not success:
	print("failed to read video")
	sys.exit(1)

