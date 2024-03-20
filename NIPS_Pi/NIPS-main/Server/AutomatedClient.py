import socket
import cv2
import numpy
#from PIL import Image
import pickle

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
TCP_IP = '169.233.221.226'#'128.114.51.113'#'169.233.251.220'#'localhost'
TCP_PORT = 5001

while(True):
    ReceiveImage = input("Enter One for RecieveImage and Zero for ReceiveVector: ")
    if int(ReceiveImage):        
        s = socket.socket()
        s.connect((TCP_IP, TCP_PORT))
        
        Message = str(1)
        s.send(bytes(Message.ljust(16), 'utf-8'))
        
        length = recvall(s, 16)
        stringData = recvall(s, int(length))
        data = numpy.frombuffer(stringData, dtype = 'uint8')
        
        s.close()
        
        decimg = cv2.imdecode(data, 1)
        im = Image.fromarray(decimg)
        im.save('C:/Users/Leo King/lking1/Capstone/IMG.png')
        cv2.imshow('SERVER', decimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    if (int(ReceiveImage) == 0):
        s = socket.socket()
        s.connect((TCP_IP, TCP_PORT))
        
        s.send(bytes('0'.ljust(16), "utf-8"))

        length = recvall(s, 16)
        stringData = recvall(s,int(length))
        with open('Test.pkl', 'rb') as f:
            pickle.loads(object, f)
        s.close()
        


