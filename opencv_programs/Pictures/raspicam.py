#!/usr/bin/env python
'''
@author Jeremy Barr
@date 5/15/2013
@brief This script will serve as a prototype for a class 
	to capture images from the new Raspberry Pi Camera Module

version 1.1: 7/11/2013
-refined raspicam options 
-added raspivid options

'''

import os
from subprocess import call
import cv

'''
sample code:
	# capture still images from camera module
	call (["raspistill -o image.jpg"], shell=True)
	# capture 5s video (default) from the camera module
	call (["raspivid -o video.h264"], shell=True)
	# capture 10s video from the camera module
	call (["raspivid -o video.h264 -t 10000"], shell=True)
	# capture 10s video from the camera module in demo mode
	call (["raspivid -o video.h264 -t 10000 -d"], shell=True)
'''

class RaspiCam:
	"""RaspiCam class used to capture images and video from 
		the Raspberry Pi Camera Board Module"""
	
	"""Define class variables"""
	''' these are the default raspistill image parameters
		For Complete list of commands enter:
		raspistill | less
		raspivid | less
	'''
	
	'''-- raspistill 2592x1944  --'''
	
	height = 1944	# default height of 1944 pixels
	width = 2592	# default width of 2592 pixels
	exposure = "off"
	AWB = "off"
	ifx = "none"    
	filename = "output.jpg"
	SAVE_DIR = os.path.dirname(os.path.abspath(__file__)) # default is current dir
	metering = None # average, spot, backlite, matrix
	vf = False      # Flip vertically
	hf = False	# Flip horizontally

	'''-- raspivid --'''
	#Please add options... at least 1 option for God sakes...
	
	"""END of class variables"""
	
	def __init__(self):
		print "RPI Cam Initialized"

	def piCapture(self, time=0):
		''' capture still images from camera module
			Must have 'sudo' to write output file to directory
		'''
		# '-n' no preview window opens, '-vf' currently flips the image vertically
		command = "sudo raspistill -n -o %s/%s -ex %s -t %d" % (self.SAVE_DIR,self.filename,self.exposure,time)
		
		# if Metering Mode is on then add to command list
		if (self.metering != None):
			command += str(" -mm %s" % self.metering)
		if (self.height != 2592):
			command += str(" -h %d" % self.height)
		if (self.width != 1944):
			command += str(" -w %d" % self.width)
		if (self.vf != False or self.vf == True):
			command += str(" -vf")
		if (self.hf != False or self.hf == True):
			command += str(" -hf")

		print "command: ", command   # print the full command in terminal
		call ([command], shell=True)
		#call (["sudo raspistill -o output.jpg -hf -t %d" % time], shell=True)
		#print "Image Captured as %s" % self.filename
		
		# OpenCV commands to return output image as CvCapture structure
		rPic = cv.LoadImage(self.filename, 1)	# 1 = CV_LOAD_IMAGE_COLOR, 
							# 2 = CV_LOAD_IMAGE_GRAYSCALE, 
							# 3 = CV_LOAD_IMAGE_UNCHANGED
		#rCapture = cv.CaptureFromFile(self.filename)
		#rPic = cv.QueryFrame(rCapture)

		return rPic

	def piVideo(self,time=0):
		''' capture 5s video (default) from the camera module 
			or input a video duration (time) in milliseconds.
		'''
		if time>0:
			call (["sudo raspivid -o video_out.h264 -t %d" % time], shell=True)
			time = time*1000 #converts to milliseconds
			print "Capturing Video for "+str(time/1000)+ " seconds"
		else:
			print "Capturing Video for 5 seconds (default)"
			call (["raspivid -o video_out.h264"], shell=True)
		
	
