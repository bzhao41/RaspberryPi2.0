#!/usr/bin/python

import cv
import cvblob
import copy
from raspicam import RaspiCam
from track_srv_blob import *
from time import sleep

cam = RaspiCam()

cam.width,cam.height = 2592/6,1944/6

image = cam.piCapture()

cv.SaveImage("Bruce_Blob.jpg", image)
img = cv.LoadImage("Bruce_Blob.jpg", 1)

blobs = cvblob.Blobs()
size = cv.GetSize(img)

hsv = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
h = cv.CreateImage(size, 8, 1)
grey = cv.CreateImage(size, 8, 1)
yuv = cv.CreateImage(size, 8, 3)
red = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
labelImg = cv.CreateImage(size,cvblob.IPL_DEPTH_LABEL, 1)

hsv_min = cv.Scalar(0,10,10,0)
hsv_max = cv.Scalar(180,255,255,0)

cv.InRangeS(img, cv.RGB(200,0,0), cv.RGB(255,225,225),red);

result = cvblob.Label(red,labelImg,blobs)
numblobs = len(blobs.keys())

avgsize = int(result/numblobs)
print str(numblobs) + " Blobs found covering " + str(result) + "px"
filtered = cv.CreateImage(cv.GetSize(img),cv.IPL_DEPTH_8U,1)
cvblob.FilterLabels(labelImg,filtered,blobs)

bigblob = cvblob.GreaterBlob(blobs)
print "largest blob is " + str(bigblob) + " which is " + str(blobs[bigblob].area + "px"

bigblobs = copy.copy(blobs)
cvblob.FilterByLabel(bigblobs,bigblob)
print str(len(bigblobs.keys())) + " blobs with label " + str(bigblob)

centroid  = cvblob.Centroid(bigblobs[bigblob])
print "centroid of blob " + str(bigblob) + " is " + str(centroid)

imgout = cv.CreateImage(cv.Getsize(img),cv.IPL_DEPTH_8U, 3)
cv.Zero(imgout)

cvblob.RenderBlobs(labelImg,blobs,img,imgout,cvblob.CV_BLOB_RENDER_COLOR|cvblob.CV_BLOB_RENDER_CENTROID|cvblob.CV_BLOB_RENDER_BOUNDING_BOX|cvblob.CV_BLOB_RENDER_ANGLE, 1.0)

print "mean color of blob " + str(bigblob) + " is " + str(cvblob.BlobMeanColor(blobs[bigblob], labelImg, img))

cv.ShowImage("filtered" , filtered)
cv.ShowImage("imgout", imgout)
cv.ShowImage("img" , img)
#cv.ShowImage('Blob', image)

cv.WaitKey(20000)
