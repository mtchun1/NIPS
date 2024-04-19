# NIPS for Pi
This directory holds all AprilTag, Calibration, and Server code for use on a Raspberry Pi 4.

## Setup
Always create and enter python environment before utilizing library.

Navigate to 
NIPS\NIPS_Pi\

Create python environment with the following command
```
$ python -m venv --system-site-packages <name_of_environment>
```
Enter the venv with
```
$ source <name_of_environment>/bin/activate
```
Next install all required libraries with
```
$ pip install opencv-python
$ pip install PyYAML
$ pip install dt-apriltags
```
To exit the environment type
```
$ deactivate
```
## AprilTags
For testing of AprilTag navigate to 
NIPS\NIPS_Pi\NIPS-main\AprilTags\lib-dt-apriltags-daffy\customTest
and use the following command
```
$ python liveTest.py
```
If you get an error about Qt wayland type
```
$ export QT_QPA_QPA_PLATFORM=xcb
```

If camera index is not found make sure usb is connected or change index for camera on line 51.

## Camera Calibration
Before detecting any AprilTags can be detected the camera must be calibrated.  This gives a camera matrix which provides:
 - fx, focal length in the x direction
 - fy, focal length in the y direction
 - cx, focal center in the x direction
 - cy, focal center in the y direction

To calibrate first take 15-20 photos of [checker board image](https://github.com/opencv/opencv/blob/4.x/doc/pattern.png) at different points in the frame.  You should also rotate the image to ensure a complete calibration.  Its recommended that this image in printed, however I pulled it up on my ipad.
Next change the width and height on lines 4 and 5 to your desired resolution.
```
width = 1280
height = 720
```
Again if camera index make sure usb is connected or change index for camera on line 3.
```
cap = cv2.VideoCapture(<index>)
```
Finally you can take these photos by running the getImages.py script.
```
$ python getImages.py
```
Press 's' to take an image.

After getting the calibration photos, go to calibration.py to set the chessboardSize and frameSize.
```
chessboardSize = (9,6)
frameSize = (1280,720)
```
Note that the size of the chessboard can be confusing, however the provided image is lited as a 9x6.  Frame size is the size you set while getting the calibration images.
Next run the following command
```
$ python calibration.py
```
This script will print out distorted camera matrix (first) and an undistored camera matrix (second).  Additionally a couple pickle files will be saved
 - cameraMatrix.pkl, Distored Camera Matrix
 - dist.pkl Distortion Matrix 

The Undistored Camera Matrix is not stored as a pkl file, however this can be added with the following line after line 75.
```
pickle.dump(newCameraMatrix, open( "newCameraMatrix.pkl", "wb" )) 
```
## Server