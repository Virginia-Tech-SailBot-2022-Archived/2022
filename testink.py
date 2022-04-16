import cv2
import numpy as np
import os
import math
import copy

pressed=False
refPt=[]

path = "/home/pi/Dataset/Samples/Training/image" + "12" + ".png"
image = cv2.imread(path)
cv2.imshow('Frame', image)