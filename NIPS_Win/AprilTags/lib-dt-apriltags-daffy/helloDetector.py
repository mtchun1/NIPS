import cv2
from dt_apriltags import Detector
import numpy as np
import os

at_detector = Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)

imagepath = 'tag48_12_00000.png'
image = cv2.imread(imagepath, cv2.IMREAD_GRAYSCALE)
tags = at_detector.detect(image)

detections = tags.detect(image)