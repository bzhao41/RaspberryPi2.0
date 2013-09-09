#!/usr/bin/python

'''
@author Jeremy Barr
@date 7/5/2013
@brief Test function to use OpenCV and cvBlobs.
'''

import cv
from raspicam import RaspiCam
import cvblob
import copy
from subprocess import call
import time

############################
''' Function findBlobs() : converts to YUV and finds all the blobs
	finds the largest blob and it's centroid.
'''
############################
def findBlobs(img,min_color,max_color,arr):
	#initialize a blobs class, and extract blobs from the greyscale image
	blobs = cvblob.Blobs()
	size = cv.GetSize(img)

	#blob = cv.CreateImage(size, 8, 1)
	hsv = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
	#yuv = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
	green = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
	labelImg = cv.CreateImage(size,cvblob.IPL_DEPTH_LABEL, 1)
	
	# the range we want to monitor
	cv.CvtColor(img,hsv,cv.CV_BGR2HSV)
	#cv.CvtColor(img,yuv,cv.CV_BGR2YCrCb)
	cv.InRangeS(hsv, min_color, max_color,green)
	
	# Smooth out the HSV_image and dilate/erode
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
                #blobarea = blobs[bigblob].area
		print "largest blob is " + str(bigblob) + " which is " + str(blobs[bigblob].area) + " px"
	
		bigblobs = copy.copy(blobs)
		cvblob.FilterByLabel(bigblobs, bigblob)
		#print str(len(bigblobs.keys())) + " blobs with label " + str(bigblob)

		# find centroid of largest blob
		centroid = cvblob.Centroid(bigblobs[bigblob])
		print "centroid of blob " + str(bigblob) + " is " + str(centroid)
                arr.append(centroid)
                cv.Circle(img,(int(centroid[0]),int(centroid[1])),50,cv.Scalar(0,0,0))
		imgOut = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 3)
		cv.Zero(imgOut)
		cvblob.RenderBlobs(labelImg, blobs, img, imgOut, cvblob.CV_BLOB_RENDER_COLOR|cvblob.CV_BLOB_RENDER_CENTROID|cvblob.CV_BLOB_RENDER_BOUNDING_BOX|cvblob.CV_BLOB_RENDER_ANGLE, 1.0)

		print "mean color for blob " + str(bigblob) + " is " + str(cvblob.BlobMeanColor(blobs[bigblob], labelImg, img))

		#cv.ShowImage("test_filtered", filtered)
		cv.ShowImage("Original", img)
		cv.ShowImage("test_rendered", imgOut)
		
	else:
		print "...Zero blobs found.\nRedefine color range for better results"
		cv.ShowImage("Original", img)

############################
''' Press ESC to continue '''
############################
def waitESC():
	k = cv.WaitKey()
	while k!=27:
		k = cv.WaitKey(33)

##########################
''' same as findblob() but outputs centroid of largest blob '''
##########################
def trackBlob(img,min_color,max_color):
	#initialize a blobs class, and extract blobs from the greyscale image
	blobs = cvblob.Blobs()
	size = cv.GetSize(img)

	#blob = cv.CreateImage(size, 8, 1)
	hsv = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
	yuv = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3)
	green = cv.CreateImage(size, cv.IPL_DEPTH_8U, 1)
	labelImg = cv.CreateImage(size,cvblob.IPL_DEPTH_LABEL, 1)
	
	# the range we want to monitor
	cv.CvtColor(img,hsv,cv.CV_BGR2HSV)
	cv.CvtColor(img,yuv,cv.CV_BGR2YCrCb)
	cv.InRangeS(yuv, min_color, max_color,green)
	
	# Smooth out the HSV_image and dilate/erode
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
		print "largest blob is " + str(bigblob) + " which is " + str(blobs[bigblob].area) + " px"
                
		bigblobs = copy.copy(blobs)
		cvblob.FilterByLabel(bigblobs, bigblob)
		#print str(len(bigblobs.keys())) + " blobs with label " + str(bigblob)
	
		# find centroid of largest blob
		centroid = cvblob.Centroid(bigblobs[bigblob])
		print "centroid of blob " + str(bigblob) + " is " + str(centroid)
	
		imgOut = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 3)
		cv.Zero(imgOut)
		cvblob.RenderBlobs(labelImg, blobs, img, imgOut, cvblob.CV_BLOB_RENDER_COLOR|cvblob.CV_BLOB_RENDER_CENTROID|cvblob.CV_BLOB_RENDER_BOUNDING_BOX|cvblob.CV_BLOB_RENDER_ANGLE, 1.0)

		print "mean color for blob " + str(bigblob) + " is " + str(cvblob.BlobMeanColor(blobs[bigblob], labelImg, img))

		#cv.ShowImage("test_filtered", filtered)
		cv.ShowImage("Original", img)
		cv.ShowImage("test_rendered", imgOut)
		
	else:
		print "...Zero blobs found.\nRedefine color range for better results"
		cv.ShowImage("Original", img)
		cv.ShowImage("YUV",green)
	return centroid

if __name__=="__main__":
    
        start = time.time()
        #Resize images
    	#img = cv.LoadImage("table1.png", 1)
	#img2 = cv.LoadImage("table2.png", 1)
	#img3 = cv.LoadImage("table3.png", 1)
        #nw = 480
        #nh = 640
        #smallimage1 = cv.CreateImage((nh,nw),img.depth,img.nChannels) 
        #smallimage2 = cv.CreateImage((nh,nw),img2.depth,img2.nChannels)
        #smallimage3 = cv.CreateImage((nh,nw),img3.depth,img3.nChannels)
        #cv.Resize(img,smallimage1,interpolation=cv.CV_INTER_CUBIC)
        #cv.Resize(img2,smallimage2,interpolation=cv.CV_INTER_CUBIC)
        #cv.Resize(img3,smallimage3,interpolation=cv.CV_INTER_CUBIC)
        #cv.SaveImage("smlTable1.jpg", smallimage1)
        #cv.SaveImage("smlTable2.jpg", smallimage2)
        #cv.SaveImage("smlTable3.jpg", smallimage3)

        
        
        #Load images from current directory
        #img = cv.LoadImage("smlTable1.jpg", 1)
        #img2 = cv.LoadImage("smlTable2.jpg", 1)
        #img3 = cv.LoadImage("smlTable3.jpg", 1)
        #img4 = cv.LoadImage("test.png",1)
        
        #Init Camera
	#cam = RaspiCam()
	#cam.width,cam.height = 640,480
	#cam.vf,cam.hf = True,True
	#imgPi = cam.piCapture()
	
        #empty array for recording purposes
        arr = []
        
        #User input fo HSV values
        #a = raw_input("Enter a hue between 0 and 180: ")
        #b = raw_input("Enter a saturation between 0 and 256: ")
        #c = raw_input("Enter a value between 0 and 256: ")
        #e = raw_input("Enter a hue between 0 and 180: ")
        #f = raw_input("Enter a saturation between 0 and 256: ")
        #g = raw_input("Enter a value between 0 and 256: ")
        
        #User inputed scalars
        #min_hsv = cv.Scalar(float(a),float(b),float(c))
        #max_hsv = cv.Scalar(float(e),float(f),float(g))

        #min and max green hsv scalars. 75 was original for min. 95 was original for max
	#min_hsvGreen = cv.Scalar(30, 100 , 100, 0)
	#max_hsvGreen = cv.Scalar(90, 255, 255, 0)
        
        #min and max red hsv: Editable
        min_hsvRed = cv.Scalar(30,100,100,0)
        max_hsvRed = cv.Scalar(90,255,255,0)

        #min and max green yuv scalars
	#min_yuvGreen = cv.Scalar(200, 80, 50)
	#max_yuvGreen = cv.Scalar(256, 110,150)

        #min and max green yuv scalars 
	#min_yuvGreen = cv.Scalar(165,136,9)
        #max_yuvGreen = cv.Scalar(116,100,80)

        #min and max blue yuv scalars
        #min_yuvBlue = cv.Scalar(75,50,120)
	#max_yuvBlue = cv.Scalar(135,125,220)
        
        #find blobs from camara
	#findBlobs(imgPi,min_yuvBlue,max_yuvBlue)
	#waitESC()
	#findBlobs(imgPi,min_yuvGreen,max_yuvGreen)
	
        #find blobs from test file
        #findBlobs(img4,min_hsv,max_hsv,arr)
        #waitESC()
        
        #user inputed:find blobs and record in array
        #findBlobs(img,min_hsv,max_hsv,arr)
	#waitESC()
	#findBlobs(img2,min_hsv,max_hsv,arr)
	#waitESC()
	#findBlobs(img3,min_hsv,max_hsv,arr)
	#waitESC()

        #find hsv green from table images and record in array
        #findBlobs(img,min_hsvGreen,max_hsvGreen,arr)
	#waitESC()
	#findBlobs(img2,min_hsvGreen,max_hsvGreen,arr)
	#waitESC()
	#findBlobs(img3,min_hsvGreen,max_hsvGreen,arr)
	#waitESC()
        
        #find yuv green in table images and record in array
	#trackBlob(img,min_yuvGreen,max_yuvGreen)
	#waitESC()
	#trackBlob(img2,min_yuvGreen,max_yuvGreen)
	#waitESC()
	#trackBlob(img3,min_yuvGreen,max_yuvGreen)
	#waitESC()
       
        #print out the contents of the array
        #print arr
        
        a = 1
        while a < 5:
            
            imageName = "/home/pi/opencv_programs/Pictures/image" +str(a) + ".jpg"
            call(["sudo raspistill -n -q 10 -t 0 -h 324 -w 432 -o " + imageName], shell = True)
            img = cv.LoadImage(imageName,1)
            findBlobs(img,min_hsvRed,max_hsvRed,arr)
            waitESC()
            print a
            a = 1+a
        
        print arr



#Notes
#Mean color is given as rgb color values
