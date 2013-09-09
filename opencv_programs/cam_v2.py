# cam_v3.py

# Jeremy Barr
# 4/29/2013
# Program uses VideoCapture(0) to grab images from camera and saves image when ENTER is pressed

import cv2, cv

capture = cv2.VideoCapture(0)

''' capture image from webcam 'capture' '''
_, img_array = capture.read()

print 'Capturing image...'
image = cv.fromarray(img_array)

print 'Saving Image...'
cv.SaveImage('foo.jpg', image)

capture.release()
print 'Capture released'