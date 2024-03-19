import cv2
import numpy
import pickle

try:
    import yaml
except:
    raise Exception('You need yaml in order to run the tests. However, you can still use the library without it.')

test_images_path = 'pictures'
parameter_file_name = 'test_info_live.yaml'

# with open(test_images_path + '/' + parameter_file_name, 'r') as stream:
#     parameters = yaml.safe_load(stream)

# cameraMatrix = numpy.array(parameters['sample_test']['K']).reshape((3,3))

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

succes, img = cap.read()

while cap.isOpened():
    succes, img = cap.read()
    cv2.imshow('Img_Uncal',img)

    # cv2.imwrite('liveVid_Uncal.png', img)
    # cv2.imread('liveVid_Uncal.png')
    h,  w = img.shape[:2]
    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))
    pickle.dump(newCameraMatrix, open(test_images_path + '/' + "newCameraMatrix.pkl", "wb" ))

    # Undistort
    dst = cv2.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    # cv2.imwrite('pictures/' + 'liveVid_Cal.png', dst)
    
    k = cv2.waitKey(5)
    if k == 27:
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('pictures/' + 'liveVid_Cal.png', dst)
        cv2.imshow('Img_cal',dst)
        print("image saved!")
    
    # cv2.imshow('Img_unCal', img)
    # cv2.imshow('Img_cal',dst)

# Release and destroy all windows before termination
cap.release()

cv2.destroyAllWindows()
