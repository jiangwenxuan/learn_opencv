from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output1.avi', fourcc, 25.0, (800, 1422))

# construct the argument parser and parse the argument
ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video', type = str, \
	help = 'path to input file')
ap.add_argument('-t', '--tracker', type = str, \
	default = 'kcf', help = 'OpenCV object tracker type')
args = vars(ap.parse_args())

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

# initialize the bounding box coordinates of the object we are going to track
initBB = None

if not args.get('video', False):
	print('[info] starting video stream...')
	vs = VideoStream(src = 0).start()
	time.sleep(1.0)
else:
	vs = cv2.VideoCapture(args['video'])

fps = None

i = 0

while True:
	i = i + 1
	frame = vs.read()
	frame = frame[1] if args.get('video', False) else frame
	if frame is None:
		break
	if i is 3:
		i = 0
		frame = imutils.resize(frame, width = 800)
		(H, W) = frame.shape[:2]

		if initBB is not None:
			(success, box) = tracker.update(frame)
			if success:
				(x, y, w, h) = [int(v) for v in box]
				cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			fps.update()
			fps.stop()

			info = [
				('tracker', args['tracker']),
				('success', 'yes' if success else 'no'),
				('fps', '{:.2f}'.format(fps.fps())),]
			for (i, (k, v)) in enumerate(info):
				text = "{}: {}".format(k, v)
				cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
					cv2.FONT_HERSHEY_SIMPLEX,  0.6, (0, 0, 255), 2)
		cv2.imshow('frame', frame)
		out.write(frame)
		key = cv2.waitKey(1) & 0xFF

		if key == ord('s'):
			initBB = cv2.selectROI('frame', frame, fromCenter = False, showCrosshair = True)
			tracker.init(frame, initBB)
			fps = FPS().start()
		elif key == ord('q'):
			break


if not args.get('video', False):
	vs.stop()

else:
	vs.release()


out.release()
cv2.destroyAllWindows()

# python try1.py --video xx.mp4 --tracker csrt
# python try1.py --tracker csrt