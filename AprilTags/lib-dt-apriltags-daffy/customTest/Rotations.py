"""
Author: Michael Chun (mtchun@ucsc.edu)

Library to do all of the rotation matrix math (uses the math and MatrixMath libraries). Euler angles are defined as
the standard [3-2-1] set of yaw, pitch, roll (in radians). Quaternions are defined as the unit normal attitude quaternion
with the first element as the scalar [q0] and the remaining 3 elements as the vector [q]. The standard rotation matrix takes
a vector in the inertial frame [NED] and transforms it to the body frame.
"""

import math
import MatrixMath

# Function: dcm2Euler(DCM)
# param: DCM – Rotation matrix [3 x 3]
# return: yaw, pitch, and roll [rad]
# brief: Extracts the Euler angles from the rotation matrix, in the form of yaw, pitch, roll corresponding to the [3,2,1] euler set.
#        Note that euler angles have a singularity at pitch = +/- pi/2 in that roll and yaw become indistinguishable.
# note: None.
# author: Michael Chun, 01.15.2024
def dcm2Euler(DCM):
    # Accounting for domain of arcsin.  Arcsin(1) = 90 while Arcsin(-1) = -90
    if(DCM[0][2] > -1 and DCM[0][2] < 1):
        return [math.atan2(DCM[0][1], DCM[0][0]),-math.asin(DCM[0][2]),math.atan2(DCM[1][2], DCM[2][2])]
    elif (DCM[0][2] >= 1):
        return [math.atan2(DCM[0][1], DCM[0][0]),-math.pi/2,math.atan2(DCM[1][2], DCM[2][2])]
    elif (DCM[0][2] <= -1):
        return [math.atan2(DCM[0][1], DCM[0][0]), math.pi/2,math.atan2(DCM[1][2], DCM[2][2])]

# Function: euler2DCM(yaw, pitch, roll)
# param: yaw – rotation about inertial down (rad)
#        pitch – rotation about intermediate y-axis (rad)
#        roll – rotation about body x-axis (rad)
# return: Direction Cosine Matrix (DCM) [3 x 3]
# brief: Create the direction cosine matrix, R, from the euler angles (assumed to be in radians). Angles are yaw,pitch,roll 
#        passed as individual arguments and in the form corresponding to the [3-2-1] Euler set. The DCM goes from inertial 
#        [I] vectors into the body frame [B].
# note: None.
# author: Michael Chun, 01.15.2024
def euler2DCM(yaw, pitch, roll):
    return [[math.cos(yaw)*math.cos(pitch), math.sin(yaw)*math.cos(pitch), -math.sin(pitch)], \
            [math.cos(yaw)*math.sin(pitch)*math.sin(roll)-math.sin(yaw)*math.cos(roll), math.sin(yaw)*math.sin(pitch)*math.sin(roll)+math.cos(yaw)*math.cos(roll), math.cos(pitch)*math.sin(roll)],\
            [math.cos(yaw)*math.sin(pitch)*math.cos(roll)+math.sin(yaw)*math.sin(roll), math.sin(yaw)*math.sin(pitch)*math.cos(roll)-math.cos(yaw)*math.sin(roll), math.cos(pitch)*math.cos(roll)]]
    
    

# Function: ned2enu(points)
# param: points – matrix of point in NED [n x 3]
# return: same set of [n x 3] points in ENU coordinates
# brief: Function changes coordinates from North-East-Down (NED) to East-North-Up (ENU). This is required because while all
#        of the dynamics and rotations are defined in NED, the graphics functions use ENU
# note: None.
# author: Michael Chun, 01.15.2024
def ned2enu(points):
    R = [[0, 1, 0], [1, 0, 0], [0, 0, -1]] # NED to ENU Rotation Matrix
    p_ENU = MatrixMath.multiply(points, R) # multiply matrix Points * R since nx3 * 3x3
    return p_ENU
    