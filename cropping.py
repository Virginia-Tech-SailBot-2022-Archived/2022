import cv2
import numpy as np
import os
import math
import copy
from typing import Final

#cap=cv2.VideoCapture('detectbuoy.avi')
pressed=False
refPt=[]
radius: Final[int] = 220


def click(event, x, y, flags, param):
	global pressed,refPt	
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt.append([x, y])
		cv2.circle(image,(x,y),radius,(0,255,0))
		pressed=True
	elif event == cv2.EVENT_LBUTTONUP:
		pressed=False
		cv2.imshow("image", image)

for i in range(20,30):
    path = "/home/pi/Dataset/Samples/Training/image" + str(i) + ".png"
    image = cv2.imread(path)
    #cv2.imshow('Frame', image)
    clone =image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click)    

    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            image = clone.copy()

        elif key == ord("c"):
            break

    r=radius
    x1=refPt[0][0]
    y1=refPt[0][1]

    #handling edge cases below
    dimensions = image.shape
    if (x1 - r <= 0):
        x1 = r + 1
    if (x1 - r >= dimensions[1]):
        x1 = dimensions[1] + 1 + r
    if (x1 + r <= 0):
        x1 = -r + 1
    if (x1 + r >= dimensions[1]):
        x1 = dimensions[1] - 1 - r
    if (y1 - r <= 0):
        y1 = r + 1
    if (y1 - r >= dimensions[0]):
        y1 = dimensions[0] + 1 + r
    if (y1 + r <= 0):
        y1 = -r + 1
    if (y1 + r >= dimensions[0]):
        y1 = dimensions[0] - 1 - r
        
    roi1 = image[ y1-r:y1+r,x1-r:x1+r]

    
    cv2.imshow("ROI", roi1)


    cv2.imwrite("/home/pi/Dataset/Samples/Buoy_%d.jpg" % (i-12),roi1)


    refPt=[]

cv2.waitKey(0)
cv2.destroyAllWindows()