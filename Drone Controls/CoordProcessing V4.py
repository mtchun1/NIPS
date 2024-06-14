"""
Jimmy Gong (jgong18@ucsc.edu)
"""

import os
import pickle
import socket
import time
import math
import keyboard

# Test with Phone:
# 0 is False
# 1 is S23U
# 2 is 1+7P
phone = 0


# TCP_IP = 'raspberrypi.local'
TCP_IP = '192.168.230.82'
TCP_PORT = 5001
class ProcessData:
    def init(self, data = 'This is the Test Pickle Message'):
        self.data = data
    def str(self): return self.data

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            print("None Type Error")
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf

# class sCoord:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y

# Galaxy S24, 2340x1080
# up = sCoord(473, 510)
# down = sCoord(473, 810)
# ccw = sCoord(320, 665)
# cw = sCoord(625, 665)
# forward = sCoord(1915, 510)
# backward = sCoord(1915, 810) 
# left = sCoord(1760, 665)
# right = sCoord(2065, 665)

rotDur = 200    #ms
horDur = 800    #ms
vertDur = 200    #ms

horiThreshShort = 0.175
horiThreshTall = 0.5
horiThresh = horiThreshShort    #meters
cylinderThreshHeight = 3
vertThresh = 0.7    #meters

downtime = 30
off_x = 0.0         #meters
off_y = 0.0         #meters

# max_circle = 150    #pixels
if (phone == 1):
    # max_circle = 70
    # mid_X = 1915
    # mid_Y = 665
    # down_joy = 810
    # down_x = 473
    # down_y = 750
    # kill_x = 1180
    # kill_y = 70
    max_circle = 70
    mid_X = 1265
    mid_Y = 430
    down_joy = 550
    down_x = 325
    down_y = 500
    kill_x = 800
    kill_y = 50
elif (phone == 2):
    max_circle = 170
    mid_X = 2525
    mid_Y = 880
    down_joy = 1160
    down_x = 595
    down_y = 1020
    kill_x = 1560
    kill_y = 107


## X_Joy, Y_Joy, Z_Joy = TwoStep(X, Y, Z, Yaw)
def TwoStep(X, Y, Z, Yaw):      #THIS SHOULD BE RADIANS
    if ((abs(X) > horiThresh) or (abs(Y) > horiThresh)):
        X_Joy = max_circle*(math.cos(Yaw)) + mid_X
        Y_Joy = max_circle*(math.sin(Yaw)) + mid_Y
        Z_Joy = 0
    elif (Z > vertThresh):
        X_Joy = 0
        Y_Joy = 0
        Z_Joy = down_joy
    else:
        X_Joy = 0
        Y_Joy = 0
        Z_Joy = 0
    return X_Joy, Y_Joy, Z_Joy

    
newCord = [0, 0, 0, 0, 0]
oldTime = 0
rCo = '\33[91m'
gCo = '\33[92m'
eCo = '\33[0m'

if (phone):
    start = "adb start-server"
    os.system(start)


while (True):
    first = time.time()
    s = socket.socket()
    s.connect((TCP_IP, TCP_PORT))
    s.send(bytes('1'.ljust(16), "utf-8"))
    length = recvall(s, 16)
    if (type(length) == bytes):
        global PickleFile
        stringData = recvall(s,int(length))
        PickleFile = pickle.loads(stringData)
    pose = PickleFile.data

    if (pose != None):
        newCord[0] = pose[1][0][0] + off_x     # X in meters
        newCord[1] = pose[1][1][0] + off_y     # Y in meters
        newCord[2] = pose[1][2][0]      # Z in meters
        newCord[3] = pose[2][0][0]      # Yaw in degrees

    realYaw = (math.pi + math.atan2(newCord[1], newCord[0]))

    if (newCord[2] > cylinderThreshHeight):     
        horiThresh = horiThreshTall         #horizontal threshold is larger when drone is higher
        vertTall = 200                      #drone decends longer when higher up
    else:
        horiThresh = horiThreshShort
        vertTall = 0

    if (math.sin(realYaw) > math.sin(math.radians(15))):
        # backDur = 300   #extra ms for the drone to fly back while front heavy for outdoor trials
        backDur = 0
    else:
        backDur = 0

    if (math.cos(realYaw) > math.cos(math.radians(30))):
        sideDur = 100
        print("Extra Side")
    else:
        sideDur = 0

    if (phone):
        X_Joy, Y_Joy, Z_Joy = TwoStep(newCord[0], newCord[1], newCord[2], realYaw)
    # time.sleep(0.5)

    if (pose == None):
        print(f"No Tag\r\n")
    else:
        if (abs(newCord[0]) < horiThresh):
            xCo = gCo
        else:
            xCo = rCo
        if (abs(newCord[1]) < horiThresh):
            yCo = gCo
        else:
            yCo = rCo
        if (abs(newCord[2]) < vertThresh):
            zCo = gCo
        else:
            zCo = rCo
            
        # print(f"X: {newCord[0]}, Y: {newCord[1]}, Z: {newCord[2]}, Yaw: {newCord[3]}\r\n")
        print(f"X: {xCo}{newCord[0]}{eCo}, Y: {yCo}{newCord[1]}{eCo}, Z: {zCo}{newCord[2]}{eCo}\r\n")

    second = time.time()
    print("seconds since Tag:", (second-first), "\r\n")

    if ((phone) and (pose != None)):
        if ((X_Joy > 0) or (Y_Joy > 0)):
            cmd = "adb shell input swipe {0} {1} {0} {1} {2}".format(X_Joy, Y_Joy, horDur+backDur+sideDur)
            os.system(cmd)
            time.sleep(2.0)
        elif (Z_Joy > 0):
            cmd = "adb shell input swipe {0} {1} {0} {1} {2}".format(down_x, Z_Joy, vertDur+vertTall)
            os.system(cmd)
            # time.sleep(0.2)
        elif (newCord[2] < vertThresh):
            print("LANDING... ")
            cmd = "adb shell input swipe {0} {1} {0} {1} {2}".format(down_x, down_y, vertDur*downtime)
            os.system(cmd)
            cmd = "adb shell input tap {0} {1}".format(kill_x, kill_y)
            os.system(cmd)
            print("LANDED.")
            break

    if (keyboard.is_pressed('ctrl+shift')):
        break
    