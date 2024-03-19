import sys
sys.path.append("..")

from dt_apriltags import Detector
#import Rotations
from datetime import datetime
import pickle

import socket
import os
import cv2
import numpy
import threading

casetype = "GetPNGtoSend"
Sample_ControlVector = [2, 0, 0]

#TCP Initialize
TCP_IP = "128.114.51.113"
TCP_PORT = 5001
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((TCP_IP, TCP_PORT))
sock.listen(5)

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return none
        buf += newbuf
        count -= len(newbuf)
    return buf

def handle_client(s):
    match casetype:
        case "GetPNGtoSend":
            capture = cv2.VideoCapture(0)
            capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            
            ret, frame = capture.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            result, imgencode = cv2.imencode('.jpg', frame, encode_param)
            data = numpy.array(imgencode)
            
            stringData = data.tobytes()
            
            s.send( bytes(str(len(stringData)).ljust(16), 'utf-8' ))
            s.send(stringData)
            s.close()
            
        case 'RX&TXControlInfo':
            ControlVectorString = ' '.join(map(str, Sample_ControlVector))
            ControlVectorByte = ControlVectorString.encode('utf-8')
            
            s.send( bytes(ControlVectorByte).ljust(16), 'utf-8' )
            s.send(ControlVectorByte)
            s.close()
            
        case _:
            s.close()

while(True):
    print('Waiting For Connection...')
    c, addr = sock.accept()
    print("Connection from", addr, '\n')
    length = recvall(c, 16)
    if (int(length) == 0):
        casetype = 'RX&TXControlInfo'
    else:
            casetype = 'GetPNGtoSend'
    threading.Thread(target = handle_client, args = (c,)).start()