import sys
import cv2
import numpy as np
import time
import imutils as util
import math
import pickle
# Function for stereo vision and depth estimation
import triangulation as tri
import csv

from matplotlib import pyplot as plt
from PIL import Image



def get_limits(color):

    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lowerLimit = hsvC[0][0][0] - 10, 100, 100
    upperLimit = hsvC[0][0][0] + 10, 255, 255

    lowerLimit = np.array(lowerLimit, dtype = np.uint8)
    upperLimit = np.array(upperLimit, dtype = np.uint8)

    return lowerLimit, upperLimit




# Open both cameras
cap_right = cv2.VideoCapture(1)                    
cap_left =  cv2.VideoCapture(0)


# Stereo vision setup parameters
frame_rate = 60    #Camera frame rate (maximum at 120 fps)
B = 25               #Distance between the cameras [cm]
f = 3.6              #Camera lense's focal length [mm]
alpha = 80        #Camera field of view in the horisontal plane [degrees]



#RANDOM VARIABLES
blue = [255, 0, 0] #blue in bgr space
lightGreen = [144, 238, 144] #light green in bgr space
yellow = [0, 255, 255]
red = [0, 0, 215]
yc = 960
xc = 960
cx1 = 1
cx = 1

pixelft = 1
xpixelft = 1
ypixelft = 1
ftm = False

cam1 = 5
cam2 = 5

#RANDOM VARIABLES

#CSV Stuff for Plotting
plot = False
x_value = 0
y_value = 0
z_value = 0
fieldnames = ["x_value", "y_value", "z_value"]

with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
    csv_writer.writeheader()



while(cap_right.isOpened() and cap_left.isOpened()):

    #CSV writing to file
    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)

        info1 = {
            "x_value": x_value,
            "y_value": y_value,
            "z_value": z_value
        }
        ###

        succes_right, frame_right = cap_right.read()
        succes_left, frame_left = cap_left.read()
        #print (frame_right.shape, ' ', frame_left.shape)
    ################## CALIBRATION #########################################################


        with open('cameraMatrix2.pkl', 'rb') as stream1:
            cameraMatrix1 = pickle.load(stream1)

        with open('dist2.pkl', 'rb') as stream2:
            dist1 = pickle.load(stream2)

        h1,  w1 = frame_right.shape[:2]
        newCameraMatrix1, roi1 = cv2.getOptimalNewCameraMatrix(cameraMatrix1, dist1, (w1,h1), 1, (w1,h1))

        h,  w = frame_left.shape[:2]
        newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix1, dist1, (w,h), 1, (w,h))

        #frame_right, frame_left = calibration.undistortRectify(frame_right, frame_left)
        dst = cv2.undistort(frame_right, cameraMatrix1, dist1, None, newCameraMatrix1)
        dst1 = cv2.undistort(frame_left, cameraMatrix1, dist1, None, newCameraMatrix1)
        #print (frame_right.shape, ' ', frame_left.shape)

        x_1, y_1, w_1, h_1 = roi
        x_2, y_2, w_2, h_2 = roi1
        dst = dst[y_1:y_1+h_1, x_1:x_1+w_1]
        dst1 = dst1[y_2:y_2+h_2, x_2:x_2+w_2]
    ########################################################################################

        # If cannot catch any frame, break
        if not succes_right or not succes_left:                    
            break

        else:

            start = time.time()
            
            # Convert the BGR image to RGB
            frame_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2RGB)
            frame_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2RGB)

            # Convert the RGB image to BGR
            frame_right = cv2.cvtColor(frame_right, cv2.COLOR_RGB2BGR)
            frame_left = cv2.cvtColor(frame_left, cv2.COLOR_RGB2BGR)


            ################## CALCULATING DEPTH #########################################################

            center_right = 0
            center_left = 0

        hsvImage = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
        hsvImage1 = cv2.cvtColor(dst1, cv2.COLOR_BGR2HSV)




        lowerLimit, upperLimit = get_limits(color=lightGreen)
        lowerLimit1, upperLimit1 = get_limits(color=lightGreen)

        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
        mask_ = Image.fromarray(mask)

        mask1 = cv2.inRange(hsvImage1, lowerLimit1, upperLimit1)
        mask1_ = Image.fromarray(mask1)


        bbox = mask_.getbbox()
        bbox1 = mask1_.getbbox()
        
        if bbox is not None:
            x1, y1, x2, y2 = bbox
            cv2.rectangle(dst, (x1, y1), (x2, y2), (0,255,0), 5)
            cx = (x2 - x1)/2 + x1
            cy = (y2 - y1)/2 + y1

            #print('\n(', x1, ',' , x2, ')') 

        if bbox1 is not None:
            x3, y3, x4, y4 = bbox1
            cv2.rectangle((dst1), (x3, y3), (x4, y4), (255,0,0), 5)
            cx1 = (x4 - x3)/2 + x3
            cy1 = (y4 - y3)/2 + y3
            #print('\n(', x3, ',' , x4, ')*') 

        if bbox1 is not None:
            if bbox is not None:
                depth = tri.find_depth(cx, cx1, frame_right, frame_left, B, f, alpha)

                cv2.putText(frame_right, "Distance: " + str(round(depth,1)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,0,0),3)
                cv2.putText(frame_left, "Distance: " + str(round(depth,1)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,0,0),3)
                # Multiply computer value with 205.8 to get real-life depth in [cm]. The factor was found manually.
        
                theta = ((-1629/2) + cx) * (80/1629)#564
                phi = ((404) - cy) * (40/808)#564
                print("x: ", str(round(depth,1)))
                print("y: ", str(round(depth,1)*math.tan(math.radians(theta))))
                print("z: ", str(round(depth,1)*math.tan(math.radians(phi))))
                #print('Theta: ',theta)
                #print('Tan: ',math.tan(math.radians(theta)))
                #print(y2, ', ', y1)
                x_value = round(depth,1)
                y_value = round(depth,1)*math.tan(math.radians(theta))
                z_value = round(depth,1)*math.tan(math.radians(phi))
                if plot == True:
                    csv_writer.writerow(info1)

        

        end = time.time()
        totalTime = end - start

        fps = 1 / totalTime
        #print("FPS: ", fps)

        cv2.putText(frame_right, f'FPS: {int(fps)}', (20,450), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,0,0), 2)
        cv2.putText(frame_left, f'FPS: {int(fps)}', (20,450), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,0,0), 2)                                   


            # Show the frames
        cv2.imshow("frame right", dst) 
        cv2.imshow("frame left", dst1)

        if cv2.waitKey(1) & 0xFF == ord('p'):
            plot = True

            # Hit "q" to close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# Release and destroy all windows before termination
cap_right.release()
cap_left.release()

cv2.destroyAllWindows()