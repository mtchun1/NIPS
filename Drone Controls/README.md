# Drone Controls
This directory holds all the necessary files to run autonomous drone control through the drone's proprietary app.

## Setup
1. Plug in the android device running the HS FPV V4 app to the host computer.

2. Turn on the drone and connect the android device to the drone's Wi-Fi.

3. Configure the correct TCP_IP which should be the same on the PI code.

4. Ensure that line 157 is set to True.
```
$ phone = True
```
5. Tap the takeoff icon on the bottom left of the android device to start up the drone and takeoff.

6. Fly the drone over the AprilTag zone.

7. Run CoordProcessing.py in terminal.
```
$ python3 CoordProcessing.py
```
8. Watch the drone take its time to automatically land on the AprilTag.

9. If you need the drone to stop automatically moving, KeyboardInturrupt the code by pressing ctrl+c in the terminal.

10. If you need the drone to stop powering its propellers for any reason, tap the red "Emergency Stop" button at the top middle of
	the android device. This will likely be used very often for safety reasons.