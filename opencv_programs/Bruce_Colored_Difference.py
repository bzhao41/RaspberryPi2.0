#!/usr/bin/python

import cv
import cvblob
from raspicam import RaspiCam
from track_srv_blob import *
from time import sleep

cam = RaspiCam()

cam.width,cam.height = 2592/6,1944/6

image1 = cam.piCapture()
cv.SaveImage("Colored_Test.jpg",image1)
capture = cv.CaptureFromFile("Colored_Test.jpg")
image1 = cv.QueryFrame(capture)
sleep(5)
image2 = cam.piCapture()
cv.SaveImage("Colored_Test2.jpg",image2)
capture2 = cv.CaptureFromFile("Colored_Test2.jpg")
image2 = cv.QueryFrame(capture2)
w,h = cv.GetSize(image1)
difference = cv.CreateImage((w,h),8,3)
cv.AbsDiff(image1,image2,difference)
cv.SaveImage("Colored_Test_Difference.jpg", difference)
cv.ShowImage('Difference', difference)
cv.WaitKey(20000)
