# NIPS
The Navigation Imaging Precision System (NIPS) aims to create autonomous landing technology using AprilTags for drones.

## Drone Controls
Directory for drone controls.  Takes the pose translation and rotation from AprilTag script and uses it to navigate in the air while it attempts to land on the AprilTag.

## NIPS_Pi
AprilTag Recognition, Calibration, and Server capability for use in entire control loop.  For use in Raspberry Pi only.

## NIPS_Win
AprilTag Recognition and Calibration for use on Windows.  Incapable of live camera feed recognition, only images.  Requires use of WSL.

## True Position
True position subsystem that tracks an object with its color and graphs its x, y, and z.