import util
import numpy as np
import cv2
import threading
from PIL import Image

blue = [255, 0, 0] #blue in bgr space
lightGreen = [144, 238, 144] #light green in bgr space
yellow = [0, 255, 255]
cap = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)

while True:
    ret,  frame = cap.read()
    ret1,  frame1 = cap1.read()

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsvImage1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)

    lowerLimit, upperLimit = util.get_limits(color=lightGreen)
    lowerLimit1, upperLimit1 = util.get_limits(color=lightGreen)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    mask_ = Image.fromarray(mask)

    mask1 = cv2.inRange(hsvImage1, lowerLimit1, upperLimit1)
    mask1_ = Image.fromarray(mask1)


    bbox = mask_.getbbox()
    bbox1 = mask1_.getbbox()
    
    if bbox is not None:
        x1, y1, x2, y2 = bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 5)
        cx = (x2 - x1)/2 + x1
        cy = (y2 - y1)/2 + y1

        print('\n(', cx, ',' , cy, ')') 

    if bbox1 is not None:
        x3, y3, x4, y4 = bbox1
        cv2.rectangle(frame1, (x3, y3), (x4, y4), (255,0,0), 5)
        cx1 = (x4 - x3)/2 + x3
        cy1 = (y4 - y3)/2 + y3
        print('\n(', cx1, ',' , cy1, ')*') 

    cv2.imshow('frame', frame)
    cv2.imshow('frame1', frame1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindow()