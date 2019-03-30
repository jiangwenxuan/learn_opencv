import cv2
import numpy as np

class Segmenter():

	def __init__(self):
		self._mask_32s = None
		self._waterImg = None

	def setMask(self, mask):
		self._mask_32s = np.int32(mask)

	def waterProcess(self, img):
		self._waterImg = cv2.watershed(img, self._mask_32s)

	def getSegmentationImg(self):
		segmentationImg = np.uint8(self._waterImg)
		return segmentationImg

	def getWaterSegmentationImg(self):
		waterSegmentationImg = np.copy(self._waterImg)
		waterSegmentationImg[self._waterImg == -1] = 1
		waterSegmentationImg = np.uint8(waterSegmentationImg)
		return waterSegmentationImg

	def mergeSegmentationImg(self, waterSegmentationImg, isWhite = False):
		_, segmentMask = cv2.threshold(waterSegmentationImg, 250, 1, cv2.THRESH_BINARY)
		segmentMask = cv2.cvtColor(segmentMask, cv2.COLOR_GRAY2BGR)
		mergeImg = cv2.multiply(frame, segmentMask)
		if isWhite is True:
			mergeImg[mergeImg == 0] = 255
		return mergeImg

def getBoundingRect(img, pattern):
	contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	x, y, w, h = cv2.boundingRect(contours[1])
	cv2.rectangle(pattern, (x, y), (x+w, y+h), (0, 0, 200), 2)

cap = cv2.VideoCapture('test.avi')
fourcc = cv2.VideoWriter_fourcc(*'MJPG')\

i = 0
all_images = []
mySegmenter = Segmenter()

while cap.isOpened():
	ret, frame = cap.read()
	i = i + 1
	if ret is True:
		if i is 3:
			i = 0
# forward image
			grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			blurImg = cv2.blur(grayImg, (3, 3))
			_, binImg = cv2.threshold(blurImg, 30, 255, cv2.THRESH_BINARY_INV)
			kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
			fgImg = cv2.morphologyEx(binImg, cv2.MORPH_RECT, kernel1)
# background image
			kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
			dilateImg = cv2.dilate(binImg, kernel2, iterations = 4)
			_, bgImg = cv2.threshold(dilateImg, 1, 128, cv2.THRESH_BINARY_INV)
# mark image
			maskImg = cv2.add(fgImg, bgImg)
			mySegmenter.setMask(maskImg)

			mySegmenter.waterProcess(frame)
			waterSegmentationImg = mySegmenter.getWaterSegmentationImg()
			outputImgWhite = mySegmenter.mergeSegmentationImg(waterSegmentationImg, True)
			kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
			dilateImg = cv2.dilate(waterSegmentationImg, kernel3)
			_, dilateImg = cv2.threshold(dilateImg, 130, 255, cv2.THRESH_BINARY)

			getBoundingRect(dilateImg, frame)
			all_images.append(frame)
			cv2.imshow('camera', frame)
			if cv2.waitKey(1) & 0xFF is ord('q'):
				break

	else:
		break

shape = all_images[0].shape
size = (shape[1], shape[0])

out = cv2.VideoWriter('output7.avi', fourcc, 20.0, size)

for img in all_images:
	out.write(img)

cap.release()
out.release()
cv2.destroyAllWindows()
