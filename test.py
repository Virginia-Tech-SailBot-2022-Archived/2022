from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2

cv2.namedWindow('Track')

#trackbar
def track(x):
    pass
cv2.createTrackbar('Hmin', 'Track', 0, 179, track);
cv2.createTrackbar('Hmax', 'Track', 10, 179, track);
cv2.createTrackbar('Smin', 'Track', 0, 255, track);
cv2.createTrackbar('Smax', 'Track', 255, 255, track);
cv2.createTrackbar('Vmin', 'Track', 0, 255, track);
cv2.createTrackbar('Vmax', 'Track', 255, 255, track);

camera = PiCamera()

camera.resolution = (1920, 1088)
camera.framerate = 24

raw_capture = PiRGBArray(camera, size=camera.resolution)

time.sleep(0.1)
counter = 0
for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    
    image = frame.array;
    
    cv2.imshow('Frame', image)
    path = '/home/pi/Dataset/Samples/Training/image' +str(counter) +'.png'
    cv2.imwrite(path, image)
    raw_capture.truncate(0)
    key = cv2.waitKey(1) & 0xFF
    counter = counter + 1
    if key == ord("q"):
        break