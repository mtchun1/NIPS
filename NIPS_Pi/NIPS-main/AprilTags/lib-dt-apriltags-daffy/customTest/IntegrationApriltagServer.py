#Apriltag - Server Integration, Pickle Transmission Test
import sys
sys.path.append("..")

from dt_apriltags import Detector
import Rotations
from datetime import datetime
import pickle
import MatrixMath
import math

import socket
<<<<<<< HEAD
import os
import numpy
import threading
=======
import numpy
import threading
import os
from CircularBuffer import RingBuffer
>>>>>>> d338725 (updated calibration, new integration code, new apriltag code)

try:
    import cv2
except:
    raise Exception('You need cv2 in order to run the demo. However, you can still use the library without it.')

try:
    from cv2 import imshow
except:
    print("The function imshow was not implemented in this installation. Rebuild OpenCV from source to use it")
    print("VIsualization will be disabled.")
    visualization = False

try:
    import yaml
except:
    raise Exception('You need yaml in order to run the tests. However, you can still use the library without it.')

#Pre-Defines BEGIN
casetype = "GetPNGtoSend"
Sample_ControlVector = [2, 0, 0]
<<<<<<< HEAD
=======
CBuff = RingBuffer(10)
>>>>>>> d338725 (updated calibration, new integration code, new apriltag code)

#Pre-Defines END

#April Tag Pre-Defines BEGIN
test_images_path = 'pictures'
parameter_file_name = 'test_info_live.yaml'
pickle_parameter_file_name = 'camera_params_pickle'
visualization = True

at_detector = Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)

with open(test_images_path + '/' + parameter_file_name, 'r') as stream:
    parameters = yaml.safe_load(stream)
    
with open(pickle_parameter_file_name+ '/' + 'cameraMatrix.pkl', 'rb') as stream1:
    cameraMatrix = pickle.load(stream1)
stream1.close()

with open(pickle_parameter_file_name+ '/' + 'dist.pkl', 'rb') as stream2:
    dist = pickle.load(stream2)
stream2.close()
    
<<<<<<< HEAD
cap = cv2.VideoCapture(0)
width = 1280
height = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
num = 0
#April Tag Pre-Defines END

=======
#April Tag Pre-Defines END

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.close()

>>>>>>> d338725 (updated calibration, new integration code, new apriltag code)
#TCP Initialize
TCP_IP = "128.114.51.113"
TCP_PORT = 5001
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
<<<<<<< HEAD
sock.bind((TCP_IP, TCP_PORT))
sock.listen(5)
=======
try:
    sock.bind((TCP_IP, TCP_PORT))
    sock.listen(5)
except:
    sock.close()
    print("FAILED")
    
cap = cv2.VideoCapture(0)
width = 1280
height = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
>>>>>>> d338725 (updated calibration, new integration code, new apriltag code)

#Class Pickle Class
class ProcessData:
    def __init__(self, data = 'No Data was Set'):
        self.data = data
    def __str__(self): return self.data
#Pickle Class End

#Function for Receiving from TCP PORT
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return none
        buf += newbuf
        count -= len(newbuf)
    return buf

#Client Handling State Machine
def handle_client(s):
    match casetype:
        case "GetPNGtoSend":
<<<<<<< HEAD
            capture = cv2.VideoCapture(0)
=======
            capture = cv2.VideoCapture(1)
>>>>>>> d338725 (updated calibration, new integration code, new apriltag code)
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
        
        case 'Apriltag':
<<<<<<< HEAD
            succes, img = cap.read()

            # img = cv2.imread(test_images_path+'/'+parameters['sample_test']['file'], cv2.IMREAD_GRAYSCALE)
            #img = cv2.imread(test_images_path+'/'+parameters['sample_test']['file'], cv2.IMREAD_GRAYSCALE)

            # cameraMatrix = numpy.array(parameters['sample_test']['K']).reshape((3,3))
            
            h,  w = img.shape[:2]
            newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))
            pickle.dump(newCameraMatrix, open(pickle_parameter_file_name + '/' + "newCameraMatrix.pkl", "wb" ))

            # Undistort
            dst = cv2.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

            # crop the image
            x, y, w, h = roi
            dst = dst[y:y+h, x:x+w]
            
            dst_g = cv2.cvtColor(dst, cv2.COLOR_RGB2GRAY)
            camera_params = ( newCameraMatrix[0,0], newCameraMatrix[1,1], newCameraMatrix[0,2], newCameraMatrix[1,2] )

            #cv2.imshow('Original image',img)

            tags = at_detector.detect(dst_g, True, camera_params, parameters['sample_test']['tag_size'])

            color_img = cv2.cvtColor(dst_g, cv2.COLOR_GRAY2RGB)

            for tag in tags:
                for idx in range(len(tag.corners)):
                    cv2.line(color_img, tuple(tag.corners[idx-1, :].astype(int)), tuple(tag.corners[idx, :].astype(int)), (0, 255, 0))

                cv2.putText(color_img, str(tag.tag_id),
                            org=(tag.corners[0, 0].astype(int)+10,tag.corners[0, 1].astype(int)+10),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.8,
                            color=(0, 0, 255))
                
                euler = Rotations.dcm2Euler(tag.pose_R)
                eulerformat = [[euler[0]], [euler[1]], [euler[2]]]
                euler_deg = numpy.array(MatrixMath.scalarMultiply(180/math.pi, eulerformat))
                
                data = ProcessData(tag.pose_t, euler_deg, datetime.now().strftime("%H%M%S"))
                Pickled_Data = pickle.dumps(data)
                s.send( bytes(str(len(Pickled_Data))).ljust(16), 'utf-8' )
                s.send(Pickled_Data)
                s.close()
                print(data)
            
        case _:
            s.close()

while(True):
    print('Waiting For Connection...')
    c, addr = sock.accept()
    print("Connection from", addr, '\n')
    length = recvall(c, 16)
    if (int(length) == 0):
        casetype = 'RX&TXControlInfo'
    else if (int(length) == 1):
        casetype = 'Apriltag'
    threading.Thread(target = handle_client, args = (c,)).start()
    
=======
            try: 
                num = 0
                succes, img = cap.read()

                # img = cv2.imread(test_images_path+'/'+parameters['sample_test']['file'], cv2.IMREAD_GRAYSCALE)
                #img = cv2.imread(test_images_path+'/'+parameters['sample_test']['file'], cv2.IMREAD_GRAYSCALE)

                # cameraMatrix = numpy.array(parameters['sample_test']['K']).reshape((3,3))
                #Calibration = datetime.now().strftime("%S")
                h,  w = img.shape[:2]
                newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))
                pickle.dump(newCameraMatrix, open(pickle_parameter_file_name + '/' + "newCameraMatrix.pkl", "wb" ))

                # Undistort
                dst = cv2.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

                # crop the image
                x, y, w, h = roi
                dst = dst[y:y+h, x:x+w]
                
                dst_g = cv2.cvtColor(dst, cv2.COLOR_RGB2GRAY)
                camera_params = ( newCameraMatrix[0,0], newCameraMatrix[1,1], newCameraMatrix[0,2], newCameraMatrix[1,2] )

                #cv2.imshow('Original image',img)

                tags = at_detector.detect(dst_g, True, camera_params, parameters['sample_test']['tag_size'])

                color_img = cv2.cvtColor(dst_g, cv2.COLOR_GRAY2RGB)
                #print("Calibration: ", datetime.now().strftime("%S") - Calibration)
                
                #Forloop = datetime.now().strftime("%S")
                for tag in tags:
                    for idx in range(len(tag.corners)):
                        cv2.line(color_img, tuple(tag.corners[idx-1, :].astype(int)), tuple(tag.corners[idx, :].astype(int)), (0, 255, 0))

                    cv2.putText(color_img, str(tag.tag_id),
                                org=(tag.corners[0, 0].astype(int)+10,tag.corners[0, 1].astype(int)+10),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.8,
                                color=(0, 0, 255))
                    
                    euler = Rotations.dcm2Euler(tag.pose_R)
                    eulerformat = [[euler[0]], [euler[1]], [euler[2]]]
                    euler_deg = numpy.array(MatrixMath.scalarMultiply(180/math.pi, eulerformat))
                    
                    pik = tag.pose_t, euler_deg, datetime.now().strftime("%f")
                    pickle.dump(pik, open( "detect.pkl", "wb" ))
                #print("Forloop: ", datetime.now().strftime("%S") - Forloop)
                with open("detect.pkl", 'rb') as f:
                    data = pickle.load(f)
                    Pickled_Data = pickle.dumps(ProcessData(data))
                    s.send( bytes(str(len(Pickled_Data)).ljust(16), 'utf-8'))
                    s.send(Pickled_Data)
                    s.close()
                    print(data)
                    
            except KeyboardInterrupt:
                sock.close()
                
            except:
                print("DIED Here")
                sock.close()

        case _:
            sock.close()

try:
    while(True):
        print('Waiting For Connection...')
        c, addr = sock.accept()
        print("Connection from", addr, '\n')
        length = recvall(c, 16)
        if (int(length) == 0):
            casetype = 'RX&TXControlInfo'
        elif (int(length) == 1):
            casetype = 'Apriltag'
        #casetype = 'Apriltag'
        #threading.Thread(target = handle_client, args = (c,)).start()
        handle_client(c)
        
except KeyboardInterrupt:
    sock.close()
    
except:
    print("Death")
    sock.close()
>>>>>>> d338725 (updated calibration, new integration code, new apriltag code)
    
    
    