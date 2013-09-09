#!/usr/bin/env python

import os
from subprocess import call
import cv2.cv as cv
import time
from raspicam import RaspiCam

start_time = time.time()

#take two pictures
call(["sudo raspistill -n -t 0 -h 324 -w 432 -o /home/pi/opencv_programs/Pictures/output.jpg"], shell = True)
time.sleep(5)
call(["sudo raspistill -n -t 0 -h 324 -w 432 -o /home/pi/opencv_programs/Pictures/output2.jpg"], shell = True)

#load two pictures and convert to greyscale
image1 = cv.CaptureFromFile("output.jpg")
image2 = cv.CaptureFromFile("output2.jpg")
query1 = cv.QueryFrame(image1)
query2 = cv.QueryFrame(image2)
grey1 = cv.CreateImage(cv.GetSize(query1),query1.depth, 1)
grey2 = cv.CreateImage(cv.GetSize(query2),query2.depth, 1)
cv.CvtColor(query1,grey1,cv.CV_RGB2GRAY)
cv.CvtColor(query2,grey2,cv.CV_RGB2GRAY)

#Absolute Difference of the two images
difference = cv.CreateImage(cv.GetSize(query1),query1.depth,1)
cv.AbsDiff(grey1,grey2,difference)
cv.SaveImage("Difference.jpg",difference)


curr_time = time.time()
print curr_time - start_time
