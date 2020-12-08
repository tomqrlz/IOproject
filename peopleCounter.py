import time

import cv2
import dlib
import numpy as np
from imutils.video import FPS

from colorDetection import colorDetection
from logs import logToFile
from model.centroidtracker import CentroidTracker
from model.trackableobject import TrackableObject


# initialize the list of class labels MobileNet SSD was trained to
# detect
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

logsList = []

# load our serialized model from disk
def analyze(input):
	model = "mobilenet_ssd/MobileNetSSD_deploy.caffemodel"
	prototxt = "mobilenet_ssd/MobileNetSSD_deploy.prototxt"
	rectsList = []
	frameList = []
	net = cv2.dnn.readNetFromCaffe(prototxt, model)

	vs = cv2.VideoCapture(input)

	# initialize the frame dimensions
	W = int(vs.get(3))
	H = int(vs.get(4))

	# instantiate our centroid tracker
	ct = CentroidTracker(maxDisappeared=50, maxDistance=60)
	trackers = []
	trackableObjects = {}

	# initialize the total number of frames processed
	totalFrames = 0
	total = 0

	# start the frames per second throughput estimator
	fps = FPS().start()
	fpsReal = vs.get(cv2.CAP_PROP_FPS)

	# loop over frames from the video stream
	while True:
		# grab the next frame
		ret, frame = vs.read()
		centroidList = []

		#the end of the video
		if input is not None and frame is None:
			break



		# convert the frame from BGR to RGB for dlib
		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		# status update
		status = "Waiting"
		rects = []

		if totalFrames % 30 == 0: #60 for test
			# set the status and initialize our new set of object trackers
			status = "Detecting"
			trackers = []

			# pass the blob through the network and obtain the detections
			blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
			net.setInput(blob)
			detections = net.forward()

			# loop over the detections
			for i in np.arange(0, detections.shape[2]):
				# extract the confidence
				confidence = detections[0, 0, i, 2]

				# minimum confidence level
				if confidence > 0.4:

					idx = int(detections[0, 0, i, 1])

					# if the class label is not a person, ignore it
					if CLASSES[idx] != "person":
						continue

					# x, y-coordinates of the bounding box for the object
					box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
					(startX, startY, endX, endY) = box.astype("int")

					tracker = dlib.correlation_tracker()
					rect = dlib.rectangle(startX, startY, endX, endY)
					tracker.start_track(rgb, rect)

					trackers.append(tracker)

		# otherwise, we should utilize our object *trackers* rather than object *detectors*
		else:
			# loop over the trackers
			for tracker in trackers:
				# set the status of our system to be 'tracking'
				status = "Tracking"

				# update the tracker and grab the updated position
				tracker.update(rgb)
				pos = tracker.get_position()

				startX = int(pos.left())
				startY = int(pos.top())
				endX = int(pos.right())
				endY = int(pos.bottom())

				rects.append((startX, startY, endX, endY))

		objects = ct.update(rects)
		rectsList.append(len(rects))

		# loop over the tracked objects
		for (objectID, centroid) in objects.items():

			# check to see if a trackable object exists for the current objectID
			to = trackableObjects.get(objectID, None)

			# if there is no existing trackable object, create one
			if to is None:
				to = TrackableObject(objectID, centroid)
				total +=1
				for x in range(len(rects)):
					color = colorDetection(frame, rects[x], W, H, centroid)
					if color:
						break
					else:
						continue

				# define timestamp frames and logs
				timestamp = str(time.strftime('%H:%M:%S', time.gmtime(round(totalFrames / fpsReal, 2))))
				logsList.append("Time: " + timestamp + ", object ID: " + str(to.objectID) + ", color: " + color + ". Total people in frame: " + str(len(rects)))

			trackableObjects[objectID] = to

			# draw both the ID of the object and the centroid of the object
			text = "ID {}".format(objectID)
			cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
			cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
			centroidList.append((centroid[0], centroid[1], objectID))
		frameList.append(centroidList)

		info = [
			("Total", len(rects)),
			("Max", max(rectsList)),
			("Status", status),
		]

		# loop over the info tuples and draw them on our frame
		for (i, (k, v)) in enumerate(info):
			text = "{}: {}".format(k, v)
			cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
				cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break

		# increment the total number of frames processed thus far and
		# then update the FPS counter
		totalFrames += 1
		fps.update()

	# stop the timer and display FPS information
	fps.stop()
	print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

	# fps = vs.get(cv2.CAP_PROP_FPS)
	#
	# for x in timestampFrames:
	# 	timestamp = str(time.strftime('%H:%M:%S', time.gmtime(round(x / fps, 2))))
	# 	timestamps.append(timestamp)

	vs.release()

	rectsList.clear()
	cv2.destroyAllWindows()
	return frameList, W, H, fpsReal

def saveVideo(output, frameList, W, H, fps, input):
	vs = cv2.VideoCapture(input)
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	writer = cv2.VideoWriter(output, fourcc, fps, (W, H), True)

	for i in range(len(frameList)):
		ret, frame = vs.read()

		if input is not None and frame is None:
			break

		for j in range(len(frameList[i])):

			text = "ID {}".format(frameList[i][j][2])
			cv2.putText(frame, text, (frameList[i][j][0] - 10, frameList[i][j][1] - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
			cv2.circle(frame, (frameList[i][j][0], frameList[i][j][1] ), 4, (0, 255, 0), -1)
		# frame
		info = [
			("Total", len(frameList[i])),
		]

		# loop over the info tuples and draw them on our frame
		for (i, (k, v)) in enumerate(info):
			text = "{}: {}".format(k, v)
			cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
				cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
		writer.write(frame)
	vs.release()
	writer.release()

def saveLogs(logsPath):
	logString = ""
	# for logs, timestamp in zip(logsList, timestamps):
	# 	logString = logString + "Time: " + str(timestamp) + ", " + logs + "\n"
	for logs in logsList:
		logString = logString + logs + "\n"
	logToFile(logsPath, logString)
	logsList.clear()
