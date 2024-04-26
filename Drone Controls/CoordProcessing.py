"""
Jimmy Gong (jgong18@ucsc.edu)
"""

import os
import pickle
import socket
import time
from datetime import datetime

TCP_IP = '128.114.51.113'
# TCP_IP = '169.233.221.226'
# TCP_IP = '169.233.251.220'
# TCP_IP = '169.233.192.251'
# TCP_IP = '192.168.100.237'
# TCP_IP = 'localhost'
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


class sCoord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

tapDur = 500    #ms
# Galaxy S24, 2340x1080
up = sCoord(473, 510)
down = sCoord(473, 810)
ccw = sCoord(320, 665)
cw = sCoord(625, 665)
forward = sCoord(1915, 510)
backward = sCoord(1915, 810)
left = sCoord(1760, 665)
right = sCoord(2065, 665)
    
horiThresh = 0.05    #meters
vertThresh = 0.00    #meters
rotThresh = 5       #degrees
downtime = 20
off_x = 0.0         #meters
off_y = 0.0         #meters

cases = ['stateX', 'stateY', 'stateZ', 'stateCheck', 'stateStop', 'stateRotAlign', 'stateLost']
nextCase = cases[3]
oldCase = cases[3]
directions = ['forward', 'backward', 'right', 'left', 'down', 'up', 'hold', 'cw', 'ccw']
dir_out = directions[6]


# dir, dist, nextCase = stateMach(X, Y, Z, Yaw, Time, nextCase)
def stateMach(X, Y, Z, Yaw, Time):
    global nextCase
    global oldCase
    global downtime
    match nextCase:
        case 'stateRotAlign':
            nextCase = cases[3]     #stateCheck
            oldCase = cases[5]      #stateRotAlign
            if (Yaw > rotThresh):
                dir_out = directions[8]     #ccw
            elif (Yaw < -rotThresh):
                dir_out = directions[7]     #cw
            else:
                dir_out = directions[6]     #hold
            return dir_out, abs(Yaw)
        case 'stateX':
            nextCase = cases[3]     #stateCheck
            oldCase = cases[0]      #stateX
            if (X > horiThresh):
                dir_out = directions[2]     #right
            elif (X < -horiThresh):
                dir_out = directions[3]     #left
            else:
                dir_out = directions[6]     #hold
            return dir_out, abs(X)
        case 'stateY':
            nextCase = cases[3]     #stateCheck
            oldCase = cases[1]      #stateY
            if (Y > horiThresh):
                dir_out = directions[1]     #backward
            elif (Y < -horiThresh):
                dir_out = directions[0]     #forward
            else:
                dir_out = directions[6]     #hold
            return dir_out, abs(Y)
        case 'stateZ':
            nextCase = cases[3]     #stateCheck
            oldCase = cases[2]      #stateZ
            if (Z > vertThresh):
                dir_out = directions[4]     #down
                nextCase = cases[3]     #stateCheck
                downtime = 3           #reset descend timer
            else:
                if (downtime == 0):
                    dir_out = directions[6]     #hold
                    nextCase = cases[4]         #stateStop
                else:
                    dir_out = directions[4]     # **needs to go down blind**, utilizing counting
                    downtime -= 1
                    print(f"\r\nDown count: {downtime}")
                    nextCase = cases[2]     #stateZ
            return dir_out, abs(Z)
        case 'stateCheck':
            if (Time == oldTime):
                nextCase = cases[6]         #stateLost
            elif ((rotThresh < Yaw) or (Yaw < -rotThresh)):
                nextCase = cases[5]         #stateRotAlign
            elif ((horiThresh < X) or (X < -horiThresh)):
                nextCase = cases[0]         #stateX
            elif ((horiThresh < Y) or (Y < -horiThresh)):
                nextCase = cases[1]         #stateY
            else:
                nextCase = cases[2]         #stateZ
            return 'check', 0
        case 'stateStop':
            nextCase = cases[4]         #stateStop EOL
            oldCase = cases[4]          #stateStop
            dir_out = directions[6]     #hold
            print(f"\r\nLanded.\r\n")
            return dir_out, 0
        case 'stateLost':
            nextCase = cases[3]         #stateCheck
            oldCase = cases[6]          #stateLost
            print(f"\r\nAprilTag not sighted.\r\n")
            dir_out = directions[6]     #hold
            return dir_out, 0
        case _:
            print(f"We got a state machine leak.")
            return


cOrder = ['X', 'Y', 'Z', 'Yaw', 'Time']
newCord = [0, 0, 0, 0, 0]
oldTime = 0
prevT = 0


# Test with Phone:
phone = False

if (phone):
    start = "adb start-server"
    os.system(start)

# s = socket.socket()
# s.connect((TCP_IP, TCP_PORT))


# s.send(bytes('1'.ljust(16), "utf-8"))

while (True):
    if (dir != 'check'):
        # for i in range(5):
        #     newCord[i] = float(input(f"New {cOrder[i]}: "))
        
        # input("--Ready for Next File--\r\nPress Enter to scan new pkl\r\n")
        # time.sleep(0.05)

        # with open('detect.pkl', 'rb') as stream1:
        #     pose = pickle.load(stream1)
        # print(pose)

        s = socket.socket()
        s.connect((TCP_IP, TCP_PORT))
        s.send(bytes('1'.ljust(16), "utf-8"))
        length = recvall(s, 16)
        if (type(length) == bytes):
            global PickleFile
            stringData = recvall(s,int(length))
            PickleFile = pickle.loads(stringData)
        # print(PickleFile.data)
        #s.close()
        pose = PickleFile.data

        if (pose == None):
            pose = [0, [[0], [0], [0]], [[0], [0], [0]], oldTime]
            pose[1][0][0] = 0
            pose[1][1][0] = 0
            pose[1][2][0] = 0
            pose[2][0][0] = 0

        # newCord[0]
        newCord[0] = pose[1][0][0] + off_x     # X in meters
        newCord[1] = pose[1][1][0] + off_y     # Y in meters
        newCord[2] = pose[1][2][0]      # Z in meters
        newCord[3] = pose[2][0][0]      # Yaw in degrees
        newCord[4] = pose[3]            # Time

    dir, dist = stateMach(newCord[0], newCord[1], newCord[2], newCord[3], newCord[4])
    oldTime = newCord[4]

    #print(f"X: {newCord[0]}, Y: {newCord[1]}, Z: {newCord[2]}, Yaw: {newCord[3]}, Time: {newCord[4]}\r\n")
    if (dir != 'check'):
        print(f"\r\nDirection: {dir}, Distance: {dist}")
        newT = int(datetime.now().strftime("%f"))
        elap = int(newT - prevT)
        # if (elap < 0):
            # elap =+ 1000000
        print("ms since Tag:", elap/1000, "\r\n")
        prevT = newT
        cmd = ''
        if (phone):
            if (dir == 'up'):
                cmd = "adb shell input swipe {0} {1} {0} {1} {2}".format(up.x, up.y, tapDur)
            elif (dir == 'down'):
                cmd = "adb shell input swipe {0} {1} {0} {1} {2}".format(down.x, down.y, tapDur)
            elif (dir == 'left'):
                cmd = "adb shell input swipe {0} {1} {0} {1} {2}".format(left.x, left.y, tapDur)
            elif (dir == 'right'):
                cmd = "adb shell input swipe {0} {1} {0} {1} {2}".format(right.x, right.y, tapDur)
            elif (dir == 'forward'):
                cmd = "adb shell input swipe {0} {1} {0} {1} {2}".format(forward.x, forward.y, tapDur)
            elif (dir == 'backward'):
                cmd = "adb shell input swipe {0} {1} {0} {1} {2}".format(backward.x, backward.y, tapDur)
            elif (dir == 'ccw'):
                cmd = "adb shell input swipe {0} {1} {0} {1} {2}".format(ccw.x, ccw.y, tapDur)
            elif (dir == 'cw'):
                cmd = "adb shell input swipe {0} {1} {0} {1} {2}".format(cw.x, cw.y, tapDur)
            
        if (cmd != ''):
            os.system(cmd)

    if (phone):
        if ((newCord[4] == 0) or (oldCase == 'stateStop')):
            kill = "adb kill-server"
            os.system(kill)
            break

