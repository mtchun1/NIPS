# NIPS
The Navigation Imaging Precision System (NIPS) aims to create autonomous landing technology using AprilTags for drones.

For live testing on the PI
cd into the NIPS-main dir

  Enter the venv with

  $ source env/bin/activate

  If you get an error about Qt wayland type
  
  $ export QT_QPA_QPA_PLATFORM=xcb

Now you can run the live test
In the dir
NIPS-main/AprilTags/lib-dt-apriltags-daffy/customTest
Run liveTest.py

  $ python liveTest.py

If camera index is not found make sure usb is connected or change index for camera on line 51