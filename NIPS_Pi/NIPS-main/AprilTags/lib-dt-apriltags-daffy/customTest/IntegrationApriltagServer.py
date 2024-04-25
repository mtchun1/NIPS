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
import os
import numpy

from picamera2 import Picamera2
from CircularBuffer import RingBuffer

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
CBuff = RingBuffer(10)
#pik = (0, 10)
#Pickled_Data = (10, 10)


#Pre-Defines END

#April Tag Pre-Defines BEGIN
test_images_path = 'pictures'
parameter_file_name = 'test_info_live.yaml'
pickle_parameter_file_name = 'camera_params_pickle_Pi'
visualization = True

with open(test_images_path + '/' + parameter_file_name, 'r') as stream:
    parameters = yaml.safe_load(stream)
    
with open(pickle_parameter_file_name+ '/' + 'cameraMatrix.pkl', 'rb') as stream1:
    cameraMatrix = pickle.load(stream1)
stream1.close()

with open(pickle_parameter_file_name+ '/' + 'dist.pkl', 'rb') as stream2:
    dist = pickle.load(stream2)
stream2.close()

family_in = parameters['usb_webcam']['family_in']
family_out = parameters['usb_webcam']['family_out']

at_detector_in = Detector(families=family_in,
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)
                       
at_detector_out = Detector(families='tagCustom48h12',
                       nthreads=1,
                       max_hamming=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)
    
cv2.startWindowThread()
width = 1280
height = 720
cap = Picamera2()
cap.configure(cap.create_preview_configuration(main={"format": 'XRGB8888', "size": (width, height)}))
cap.start()
num = 0

#TCP Initialize
TCP_IP = "128.114.51.113"
TCP_PORT = 5001
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((TCP_IP, TCP_PORT))
    sock.listen(5)
except:
    sock.close()
    print("FAILED")
    

#Class Pickle Class
class ProcessData:
    def __init__(self, data = None):
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
        case 'Apriltag':
            try: 
                num = 0
                img = cap.capture_array()
                
                h,  w = img.shape[:2]
                newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))
                # Save pickle for new Camera Matrix
                #pickle.dump(newCameraMatrix, open(pickle_parameter_file_name + '/' + "newCameraMatrix.pkl", "wb" ))

                # Undistort
                dst = cv2.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

                # crop the image
                x, y, w, h = roi
                dst = dst[y:y+h, x:x+w]
                
                dst_g = cv2.cvtColor(dst, cv2.COLOR_RGB2GRAY)
                camera_params = ( newCameraMatrix[0,0], newCameraMatrix[1,1], newCameraMatrix[0,2], newCameraMatrix[1,2] )

                #cv2.imshow('Original image',img)

                tags = at_detector_out.detect(dst_g, True, camera_params, parameters['usb_webcam']['tag_size'])
                tags = tags + at_detector_in.detect(dst_g, True, camera_params, parameters['usb_webcam']['tag_size'])

                color_img = cv2.cvtColor(dst_g, cv2.COLOR_GRAY2RGB)
                #print("Calibration: ", datetime.now().strftime("%S") - Calibration)
                Pickled_Data = 0
                #Forloop = datetime.now().strftime("%S")
                for tag in tags:
                    # Draw Box around AprilTag
                    for idx in range(len(tag.corners)):
                        cv2.line(color_img, tuple(tag.corners[idx-1, :].astype(int)), tuple(tag.corners[idx, :].astype(int)), (0, 255, 0))

                    cv2.putText(color_img, str(tag.tag_id),
                                org=(tag.corners[0, 0].astype(int)+10,tag.corners[0, 1].astype(int)+10),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=0.8,
                                color=(0, 0, 255))
                    
                    # Rotation Matrix to Euler Angles of tag
                    euler = Rotations.dcm2Euler(tag.pose_R)
                    eulerformat = [[euler[0]], [euler[1]], [euler[2]]]
                    euler_deg = numpy.array(MatrixMath.scalarMultiply(180/math.pi, eulerformat))
                    
                    # Data inside Pickle
                    pik = tag.pose_t, euler_deg, datetime.now().strftime("%f")
                
                    pickle.dump(pik, open( "detect.pkl", "wb" ))
                    Pickled_Data = pickle.dumps(ProcessData(pik))
                    
                if len(tags) == 0:
                    print("No Tag")
                    Pickled_Data = pickle.dumps(ProcessData())
                #print("Forloop: ", datetime.now().strftime("%S") - Forloop)
                #with open("detect.pkl", 'rb') as f:
                    #data = pickle.load(f)
                    #print(data) 
                
                s.send( bytes(str(len(Pickled_Data)).ljust(16), 'utf-8'))
                s.send(Pickled_Data)
                s.close()
                cv2.imshow('Detected tags', color_img)
    #cv2.imwrite(test_images_path + '/' + 'detectedTag.png', color_img)
                    
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
        if (int(length) == 1):
            casetype = 'Apriltag'
        #casetype = 'Apriltag'
        #threading.Thread(target = handle_client, args = (c,)).start()
        handle_client(c)
        k = cv2.waitKey(2)
        if k == 27:
            cv2.destroyAllWindows()
            break
        
except KeyboardInterrupt:
    print("Keyboard Interrupted Properly")
    sock.close()
    
except:
    print("Death")
    sock.close()
    
    
    
