'''
@author Jeremy Barr
@date 7/11/2013
@brief Script runs the RaspiStill command with OpenCV and cvBlob integration.
'''

import cv
import cvblob
from raspicam import RaspiCam
from track_srv_blob import *
#from subprocess import call
#import os

# initialize the class
cam = RaspiCam()
cam.width,cam.height = 640,480
cam.vf,cam.hf = True,True
# capture image from Raspi camera
frame = cam.piCapture()

print 'Captured...'
#cv.ShowImage("RaspiCam",frame)

# filter the desired color
#min_red = cv.Scalar(0,50,50,0)
#max_red = cv.Scalar(13,255,255,0)
min = cv.Scalar(0,50,50,0)
max = cv.Scalar(13,255,255,0)
#min_blue = cv.Scalar(75,50,100)
#max_blue = cv.Scalar(135,125,225)

# find blobs in the image within the color range
#findBlobs(frame,min_blue,max_blue)
#findBlobs(frame, min_red, max_red)
findBlobs(frame,min,max)
waitESC() # press ESC to close windows and end program

cv.DestroyWindow("RaspiCam")

