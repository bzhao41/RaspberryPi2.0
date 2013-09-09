'''
@author/ Jeremy Barr
@date 5/8/2013
@brief Program detects blobs within an image and displays the blob
Future: display centroid of blob
'''

import cv2.cv as cv
#import SimpleCV as scv
import numpy as np

def run():
	# Capture image as CvCapture object
	capture = cv.CaptureFromFile('blob.jpeg')

	# get image from capture
	image = cv.QueryFrame(capture)

	# Smooth to get rid of false positives
	cv.Smooth(image,image,cv.CV_GAUSSIAN,19,0)

	# Display smoothed image
	cv.ShowImage('Blobs',image)

	findBlobs(image)

	cv.WaitKey(10000)

#def findBlobs(img):

# not finished
	

