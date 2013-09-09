#!/usr/bin/python
'''
@author Jeremy Barr
@date 5/15/2013
@brief Script to test RaspiCam class and overlay text over original image and greyscale image
'''
import cv
from raspicam import RaspiCam

# initialize the class
cam = RaspiCam()

#cam.width,cam.height = 2592/2,1944/2	# half size image
cam.width,cam.height = 2592/6,1944/6
# capture image from Raspi camera
image = cam.piCapture()
#capture = cv.CaptureFromFile(file)
#image = cv.QueryFrame(capture)

# font options
w,h = cv.GetSize(image)
#font_h = 2
font_h = .75
#font_w = 2
font_w = .75
#thickness = 2
thickness = 1
line_type = 8  # 8 (or omitted) 8-connected line
	       # 4 4-connected line
	       # CV_AA antialiased line
# create font
font = cv.InitFont(cv.CV_FONT_HERSHEY_PLAIN,font_h,font_w,0,thickness,line_type)
color = cv.CV_RGB(255,255,255)
cv.PutText(image,"This image was taken using the\n Raspberry Pi Camera Module", (50,h-50),font,color)
cv.SaveImage("original.jpg",image)
print "Saving image with overlayed text as 'original.jpg'"
cv.ShowImage("ORIGINAL",image)
print "converting to greyscale"

# Convert image to greyscale
grey = cv.CreateImage((w,h),8,1)
cv.CvtColor(image,grey,cv.CV_RGB2GRAY)
cv.ShowImage("grey", grey)
cv.SaveImage('greyscale.jpg',grey)
print "Image saved as 'greyscale.jpg'"
# capture video for default 5s
#vid = cam.piVideo()
#capture video for 10 seconds
#more_vid = cam.piVideo(10000)

print "Press any Key to continue..."
cv.WaitKey(20000)
