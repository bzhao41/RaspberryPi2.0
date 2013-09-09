#!/usr/bin/python

'''
@author Jeremy Barr
@date 5/7/2013
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

#load the blob image from the Current folder
#img = cv.LoadImage("blob_1.png", 1)
#img = cv.LoadImage("blob_11.png", 1)
img = cv.LoadImage("test.png", 1)
#initialize a blobs class, and extract blobs from the greyscale image
blobs = cvblob.Blobs()
size = cv.GetSize(img)

#blob = cv.CreateImage(size, 8, 1)
hsv = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
h = cv.CreateImage(size, 8, 1)
grey = cv.CreateImage(size, 8, 1)
yuv = cv.CreateImage(size, 8, 3)
red = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
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
hsv_min = cv.Scalar(0, 10, 10, 0)
hsv_max = cv.Scalar(180, 255, 255, 0)
#cv.InRangeS(hsv, hsv_min, hsv_max,red);

cv.InRangeS(img, cv.RGB(200,0,0), cv.RGB(255,225,225),red);

result = cvblob.Label(red, labelImg, blobs)
numblobs = len(blobs.keys())

# Average Size of Blobs
avgsize = int(result / numblobs)
print str(numblobs) + " blobs found covering " + str(result) + "px"
filtered = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 1)
cvblob.FilterLabels(labelImg, filtered, blobs)

# Largest Blob size
bigblob = cvblob.GreaterBlob(blobs)
print "largest blob is " + str(bigblob) + " which is " + str(blobs[bigblob].area) + " px"


bigblobs = copy.copy(blobs)
cvblob.FilterByLabel(bigblobs, bigblob)
print str(len(bigblobs.keys())) + " blobs with label " + str(bigblob)

# find centroid of largest blob
centroid = cvblob.Centroid(bigblobs[bigblob])
print "centroid of blob " + str(bigblob) + " is " + str(centroid)

imgOut = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 3)
cv.Zero(imgOut)
cvblob.RenderBlobs(labelImg, blobs, img, imgOut, cvblob.CV_BLOB_RENDER_COLOR|cvblob.CV_BLOB_RENDER_CENTROID|cvblob.CV_BLOB_RENDER_BOUNDING_BOX|cvblob.CV_BLOB_RENDER_ANGLE, 1.0)

print "mean color for blob " + str(bigblob) + " is " + str(cvblob.BlobMeanColor(blobs[bigblob], labelImg, img))

cv.ShowImage("test_filtered", filtered)
cv.ShowImage("test_rendered", imgOut)
cv.ShowImage("Original", img)


k = cv.WaitKey()
while k!=27:
	k = cv.WaitKey(33)
