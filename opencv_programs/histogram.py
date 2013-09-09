#!/usr/bin/python

'''
@author Jeremy Barr
@date 5/27/2013
@brief Test program to use OpenCV and cvBlobs.

Notes:
	-To determine the range (variance) use:
	 	cv.cvInRangeS(hsv_input,hsv_min,hsv_max, output)
	where hsv_min and hsv_max are cvScalar(h,s,v) color values
	(h/2)...180 (degrees)
	s.......255
	v.......255
	source: http://stackoverflow.com/questions/7950744/opencv-color-identification

'''

import cv2
import numpy as np
from raspicam import *



cam = RaspiCam()
cam.width,cam.height = 640,480
imgPi = cam.piCapture()
img = cv2.imread('output.jpg')

h = np.zeros((cam.width,cam.height,3))

bins = np.arange(256).reshape(256,1)
color = [ (255,0,0),(0,255,0),(0,0,255) ]

for ch, col in enumerate(color):
    hist_item = cv2.calcHist([img],[ch],None,[256],[0,255])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    hist=np.int32(np.around(hist_item))
    pts = np.column_stack((bins,hist))
    cv2.polylines(h,[pts],False,col)

h=np.flipud(h)

cv2.imshow('colorhist',h)
cv2.waitKey(0)

