import cv2
from picamera2 import Picamera2

cv2.startWindowThread()
width = 1280
height = 720
cap = Picamera2()
cap.configure(cap.create_preview_configuration(main={"format": 'XRGB8888', "size": (width, height)}))
cap.start()
num = 0

while True:

    img = cap.capture_array()

    k = cv2.waitKey(5)

    if k == 27:
        break
    elif k == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('images/img' + str(num) + '.png', img)
        print("image saved!")
        num += 1

    cv2.imshow('Img',img)

# Release and destroy all windows before termination
cap.release()

cv2.destroyAllWindows()
