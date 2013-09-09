#!/usr/bin/python

import cv
from raspicam import RaspiCam
import cvblob
from track_srv_blob import *
from time import sleep
from time import time
from subprocess import call

start_time = time()
# initialize the class
cam = RaspiCam()


#cam.width,cam.height = 2592/2,1944/2	# half size image
cam.width,cam.height = 2592/6,1944/6
# capture image from Raspi camera
image = cam.piCapture()

cv.SaveImage("original.jpg",image)
#converting to greyscale
capture = cv.CaptureFromFile("original.jpg")
image = cv.QueryFrame(capture)
no_of_bits = 8
channels = 1
w,h = cv.GetSize(image)
grey = cv.CreateImage((w,h),no_of_bits,channels)
cv.CvtColor(image,grey,cv.CV_RGB2GRAY)
cv.SaveImage("O_Grey.jpg", grey)
#pause before taking second picture
sleep(5)
#Second picture being converted to greyscale
image = cam.piCapture()
cv.SaveImage("notoriginal.jpg",image)
capture = cv.CaptureFromFile("notoriginal.jpg")
image = cv.QueryFrame(capture)
w,h = cv.GetSize(image)
grey2 = cv.CreateImage((w,h),no_of_bits,channels)
cv.CvtColor(image,grey2,cv.CV_RGB2GRAY)
cv.SaveImage("NO_Grey.jpg",grey2)
cv.ShowImage('Grey',grey)
cv.ShowImage('Grey2',grey2)

#Getting the difference between the two pictures
#The areas that are black means no change
grey3 = cv.CreateImage((w,h), no_of_bits,channels)
cv.AbsDiff(grey,grey2,grey3)
cv.SaveImage("Difference.jpg", grey3)
end_time = time()
print end_time - start_time
#cv.ShowImage('difference',grey3)
#print "Press any Key to continue..."
#cv.WaitKey(200000)
