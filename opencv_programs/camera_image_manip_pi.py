'''
@author Jeremy Barr
@date 5/1/2013
@brief Test program using OpenCV Python and raspicam. Background subtraction from camera images.
'''

import cv
from raspicam import RaspiCam

# capture image from camera
#capture = cv.CaptureFromCAM(0)
# Wait 200ms to initialize capture and take an image
#cv.WaitKey(200)
#frame = cv.QueryFrame(capture)
capture = RaspiCam()
frame = capture.piCapture()


''' frame gets copied into temp and then smoothed using CV_BLUR
CV_BLUR: linear convolution with size1 X size2 box kernel (all 1's) 
   	 with subsequent scaling by 1/(size1 * size2)
'''
temp = cv.CloneImage(frame)
cv.Smooth(temp,temp,cv.CV_BLUR,5,5)

while True:
	frame = cv.QueryFrame(capture)
	cv.AbsDiff(frame,temp,frame)
	cv.ShowImage('Original',frame)
	cv.ShowImage('Abs Diff',temp)
	c = cv.WaitKey(2)
	if c == 27:	# Break if user enters ESC
		break
