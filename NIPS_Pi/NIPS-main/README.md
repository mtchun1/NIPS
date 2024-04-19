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

If camera index is not found make sure usb is connected or change index for camera on line 51