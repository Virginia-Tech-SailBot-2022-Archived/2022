import cv2
import numpy as np

'''
To run, run the file with the weights, names and config in the same folder.
To exit, press escape.
@author: Sarthak Shrivastava
@version: 2021-02-09
'''

# load yolo
net = cv2.dnn.readNet("./yolov3-tiny.weights", "./yolov3-tiny.cfg")

#classes stores all the categories of objects we can detect
classes = []
with open("./coco.names", 'r') as f:
    classes = f.read().splitlines()

#names of the layers goes in layer_names
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

#video capture from default computer video source
cap = cv2.VideoCapture(0)


# loading image from video source cap

while True:
    _, img = cap.read()
    #storing the height, width and number of channels of original image
    height, width, channels = img.shape

    #making a blob to run our yolo algorithm on
    blob = cv2.dnn.blobFromImage(img, 1/255, (320, 320), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)
    # forward to outs

    #boxes, confidences and class_ids are an array of the boxes (size of box),
    #confidences (confidence level) and class_ids (type of object) detected
    boxes = []
    confidences = []
    class_ids = []

    #for every output layer (out) in our forwarded output_layers (outs)
    for out in outs:
        #for every detection made in each output layer
        for detection in out:
            scores = detection[5:]
            #detection's first few values contain info on height, width, size etc
            #scores contains all the recognition scores for every type of object we can detect
            class_id = np.argmax(scores)
            #class_id stores the name of the class with highest recognition score
            confidence = scores[class_id]
            #confidence stores the highest recognition score value (aka our confidence)
            #we have a very low limit to the confidence minimum (0.3) here, this might be moved up or down later
            if confidence > 0.3:
                # Object detected.
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                #center_x is center of detected object
                #x is the horizontal space the object occupies
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
            # cv2.rectangle(img, (x,y),(x+w, y+h), (0,255,0), 2)
            # cv2.circle(img, (center_x, center_y), 10, (0, 255, 0), 2)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    #this line is used to supress multiple detections of same object


    font = cv2.FONT_HERSHEY_PLAIN
    #print(len(boxes))
    for i in range(len(boxes)):
        #for every box/object detected
        if i in indexes:
            #if the box detected was NOT suppressed
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            recognition_score = str(round(confidences[i],2))
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, label, (x, y + 30), font, 2, (255,255, 255), 2)
            cv2.putText(img, recognition_score, (x, y+60), font, 2, (255,255,255),2)
            #then draw a rectangle on it

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break
    #if user presses esc break from the loop

cap.release()
cv2.destroyAllWindows()
#^^ showing the image