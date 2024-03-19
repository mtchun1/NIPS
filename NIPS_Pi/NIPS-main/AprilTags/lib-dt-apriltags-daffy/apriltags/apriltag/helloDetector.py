import cv2

import numpy as np
from apriltag import apriltag

imagepath = 'tag48_12_00000.png'
image = cv2.imread(imagepath, cv2.IMREAD_GRAYSCALE)
detector = detector.detect(image)

detections = detector.detect(image)