import cv2
import numpy as np
import imutils

def colorDetection(frame, rects, W, H, centroid):

    cX = int((rects[0] + rects[2]) / 2.0)
    cY = int((rects[1] + rects[3]) / 2.0)
    rectsCentroid = [cX, cY]
    centroid = np.ndarray.tolist(centroid)

    centroid = list(centroid)
    rectsCentroid = list(rectsCentroid)
    rects = list(rects)
    if not rectsCentroid == centroid:
        return None
    else:
        if rects[0] < 0:
            rects[0] = 1
        elif rects[1] < 0:
            rects[1] = 1
        elif rects[2] > W:
            rects[2] = W-1
        elif rects[3] > H:
            rects[3] = H-1
        frame = cv2.resize(frame, (W, H))
        frame = frame[rects[1]:rects[3], rects[0]:rects[2]]
        frame = frame[int(0.1*frame.shape[0]):int(0.7*frame.shape[0]), int(0.2*frame.shape[1]):int(0.8*frame.shape[1])]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_green = np.array([40, 70, 80])
        upper_green = np.array([70, 255, 255])

        lower_red = np.array([0, 50, 125])
        upper_red = np.array([20, 255, 255])
        lower_red1 = np.array([220, 50, 125])
        upper_red1 = np.array([255, 255, 255])

        lower_blue = np.array([90, 60, 50])
        upper_blue = np.array([150, 255, 255])

        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_green, upper_green)
        mask3 = cv2.inRange(hsv, lower_red, upper_red)
        mask4 = cv2.inRange(hsv, lower_blue, upper_blue)

        cnts1 = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts1 = imutils.grab_contours(cnts1)

        cnts2 = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts2 = imutils.grab_contours(cnts2)

        cnts3 = cv2.findContours(mask3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts3 = imutils.grab_contours(cnts3)

        cnts4 = cv2.findContours(mask4, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts4 = imutils.grab_contours(cnts4)

        area1 = []
        area2 = []
        area3 = []
        area4 = []

        for c in cnts1:
            area1.append(cv2.contourArea(c))
            #RED

        for c in cnts2:
            area2.append(cv2.contourArea(c))
            #GREEN

        for c in cnts3:
            area3.append(cv2.contourArea(c))
            #RED

        for c in cnts4:
            area4.append(cv2.contourArea(c))
            #BLUE


        if not area1:
            area1.append(0)
        if not area2:
            area2.append(0)
        if not area3:
            area3.append(0)
        if not area4:
            area4.append(0)

        if max(max(area2), max(area3), max(area4)) < 100:
            return "not detected"
        elif max(area2) > max(area3) and max(area2) > max(area4):
            return "green"
        elif (max(area3) > max(area2) and max(area3) > max(area4)) or (max(area1) > max(area2) and max(area1) > max(area4)):
            return "red"
        elif max(area4) > max(area3) and max(area4) > max(area3):
            return "blue"

