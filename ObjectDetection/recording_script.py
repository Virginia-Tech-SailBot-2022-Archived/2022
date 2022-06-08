import cv2
import numpy as np
import time
import picamera

from threading import Thread

cv2.namedWindow('Track')
cv2.namedWindow('Track2')

video = cv2.VideoCapture(0)
video2 = cv2.VideoCapture(1)

frame_width = int(video.get(3))
frame_height = int(video.get(4))
size = (frame_width, frame_height)

frame_width2 = int(video2.get(3))
frame_height2 = int(video2.get(4))
size2 = (frame_width2, frame_height2)

i = 0
# Below VideoWriter object will create
# a frame of above defined The output
# is stored in 'output.avi' file.
#result = cv2.VideoWriter('pi_camera_data.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
#result2 = cv2.VideoWriter('web_cam_data.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
while(True):
    i = i+1
    ret, frame = video.read()
    ret2, frame2 = video2.read()
    if ret2 == True:
        cv2.imshow('Track2',frame2)
        cv2.imwrite('/home/pi/dataset/webcam/frame%d.png' %i, frame2)
    if ret == True:
        
        # Write the frame into the
        # file 'output.avi'
        #result.write(frame)

        # Display the frame
        # saved in the file
        cv2.imshow('Frame', frame)
        cv2.imwrite('/home/pi/dataset/picam/frame%d.png' %i, frame)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release
# the video capture and video
# write objects
video.release()
result.release()

# Closes all the frames
cv2.destroyAllWindows()

print("The video was successfully saved")