#!/usr/bin/python

'''
@author Jeremy Barr
@date 5/27/2013
@brief Test program to use OpenCV and cvBlobs.

Future Notes:
	-To determine the range (variance) use:
	 	cv.cvInRangeS(hsv_input,hsv_min,hsv_max, output)
	where hsv_min and hsv_max are cvScalar(h,s,v) color values
	(h/2)...180 (degrees)
	s.......255
	v.......255
	source: http://stackoverflow.com/questions/7950744/opencv-color-identification

'''

import cv
import cvblob
import copy
import numpy as np

#load the blob image from the Current folder
#img = cv.LoadImage("table1.png", 1)
#img = cv.LoadImage("table2.png", 1)
#img = cv.LoadImage("table3.png", 1)
#img = cv.LoadImage("test.png", 1)
img = cv.LoadImage("test.png",1)

#initialize a blobs class, and extract blobs from the greyscale image
blobs = cvblob.Blobs()
size = cv.GetSize(img)

#blob = cv.CreateImage(size, 8, 1)
hsv = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
h = cv.CreateImage(size, 8, 1)
grey = cv.CreateImage(size, 8, 1)
yuv = cv.CreateImage(size, 8, 3)
green = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
labelImg = cv.CreateImage(size,cvblob.IPL_DEPTH_LABEL, 1)

'''
cv.CvtColor(img,hsv,cv.CV_BGR2HSV)
cv.CvtColor(img,yuv,cv.CV_BGR2YCrCb)
cv.Split(hsv,h,None,None,None) # h,s,v,none
cv.ShowImage('H',h)
cv.Threshold(h, grey, 225, 255, cv.CV_THRESH_BINARY)
cv.ShowImage('Thresh',grey)
'''
  
# the range we want to monitor
hmin = 50
hrange = 50
min_green = cv.Scalar(hmin, 100, 100, 0)
max_green = cv.Scalar(hmin+hrange, 256, 256, 0)
#cv.Smooth(img, img, cv.CV_GAUSSIAN)
#cv.Smooth(img, img, cv.CV_GAUSSIAN)
cv.CvtColor(img,hsv,cv.CV_BGR2HSV)

cv.InRangeS(hsv, min_green, max_green,green)
#cv.InRangeS(img, cv.RGB(200,230,200), cv.RGB(250,256,250),green);

''' Smooth out the HSV_image and dilate/erode'''
cv.Smooth(green, green, cv.CV_BLUR)
cv.Dilate(green,green)
cv.Erode(green,green)


result = cvblob.Label(green, labelImg, blobs)
numblobs = len(blobs.keys())

if (numblobs > 0):
	# Average Size of Blobs
	avgsize = int(result / numblobs)
	print str(numblobs) + " blobs found covering " + str(result) + "px"
	filtered = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 1)
	cvblob.FilterLabels(labelImg, filtered, blobs)

	# Largest Blob size
	bigblob = cvblob.GreaterBlob(blobs)
	print "largest blob is " + str(bigblob) + " which is " + str(blobs	[bigblob].area) + " px"
	
	bigblobs = copy.copy(blobs)
	cvblob.FilterByLabel(bigblobs, bigblob)
	#print str(len(bigblobs.keys())) + " blobs with label " + str(bigblob)
	
	# find centroid of largest blob
	centroid = cvblob.Centroid(bigblobs[bigblob])
	print "centroid of blob " + str(bigblob) + " is " + str(centroid)
	
	imgOut = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 3)
	cv.Zero(imgOut)
	cvblob.RenderBlobs(labelImg, blobs, img, imgOut, cvblob.CV_BLOB_RENDER_COLOR|cvblob.CV_BLOB_RENDER_CENTROID|	cvblob.CV_BLOB_RENDER_BOUNDING_BOX|cvblob.CV_BLOB_RENDER_ANGLE, 1.0)

	print "mean color for blob " + str(bigblob) + " is " + str	(cvblob.BlobMeanColor(blobs[bigblob], labelImg, img))

	#cv.ShowImage("test_filtered", filtered)
	cv.ShowImage("Original", img)
	cv.ShowImage("test_rendered", imgOut)
	
	k = cv.WaitKey()
	while k!=27:
		k = cv.WaitKey(33)
else:
	print "Zero blobs found..."
	k = cv.WaitKey(0)
