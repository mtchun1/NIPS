# Flight Monitoring System
This directory holds all the necessary files to run color tracking, triangulation, and live plotting.

## Setup
1. Fix cameras at 2m high a certain distance from AprilTag landing platform such that it is within view of both cameras.

2. Place drone on platform at center and press [button] to set landing point on xyz graph to (0, 0, 0).

3. Create virtual environment. Install and import required libraries:
	-sys
	-openCV
	-numpy
	-time
	-imutils
	-math
	-pickle
	-csv
	-matplotlib
	-PIL

4. Ensure that lines 34 and 35 are set to the correct cameras according to left and right.

$ cap_right = cv2.VideoCapture(1)                    
$ cap_left =  cv2.VideoCapture(0)

5. Run stereoVision.py in terminal.

$ python3 stereoVision.py

6. Run livePlot.py in terminal.

$ python3 livePlot.py

7. Press 'p' to begin tracking and plotting data.

8. Store data in data.csv in another folder and delete contents below 'x_value,y_value,z_value' to reset
