import sys
sys.path.append("..")

from dt_apriltags import Detector
import Rotations
import numpy
from datetime import datetime
import os
import pickle

test_images_path = 'pictures'
parameter_file_name = 'test_info_live.yaml'

visualization = True
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

at_detector = Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)

with open(test_images_path + '/' + parameter_file_name, 'r') as stream:
    parameters = yaml.safe_load(stream)
    
with open(test_images_path + '/' + 'cameraMatrix.pkl', 'rb') as stream1:
    cameraMatrix = pickle.load(stream1)
stream1.close()

with open(test_images_path + '/' + 'dist.pkl', 'rb') as stream2:
    dist = pickle.load(stream2)
stream2.close()
    
cap = cv2.VideoCapture(0)
width = 1280
height = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
num = 0

#### test WITH THE SAMPLE IMAGE ####
while True:
    print("\n\nTESTING WITH A SAMPLE IMAGE")
    succes, img = cap.read()

    # img = cv2.imread(test_images_path+'/'+parameters['sample_test']['file'], cv2.IMREAD_GRAYSCALE)
    #img = cv2.imread(test_images_path+'/'+parameters['sample_test']['file'], cv2.IMREAD_GRAYSCALE)

    # cameraMatrix = numpy.array(parameters['sample_test']['K']).reshape((3,3))
    
    h,  w = img.shape[:2]
    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))
    pickle.dump(newCameraMatrix, open(test_images_path + '/' + "newCameraMatrix.pkl", "wb" ))

    # Undistort
    dst = cv2.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    
    dst_g = cv2.cvtColor(dst, cv2.COLOR_RGB2GRAY)
    camera_params = ( newCameraMatrix[0,0], newCameraMatrix[1,1], newCameraMatrix[0,2], newCameraMatrix[1,2] )

    cv2.imshow('Original image',dst_g)

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
        pik = tag.pose_t, euler, datetime.now().strftime("%H%M%S")
        print(pik)
        pickle.dump(pik, open( "detect.pkl", "wb" ))


    cv2.imshow('Detected tags', color_img)

    k = cv2.waitKey(5)

    if k == 27:
        cv2.destroyAllWindows()
        break
