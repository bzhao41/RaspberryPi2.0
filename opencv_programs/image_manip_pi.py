'''
@author Jeremy Barr
@date 5/1/2013

@brief Test program that uses OpenCV Python to manipulate images loaded as 
a 'CvCapture' structure and loaded as a 'CvMat' structure
'''

import cv
from raspicam import *
# load image as CvMat structure
#capture = cv.LoadImage('picture.png',cv.CV_LOAD_IMAGE_COLOR)

# load image as CvCapture structure. Used for capturing a video from a file also.
#capture2 = cv.CaptureFromFile('image.png')

# load image as CvCapture structure from RaspiCam class (raspi cam module)
cam = RaspiCam()
cam.width,cam.height = 648,486 # 1/4 scale
#cam.scale = 0.25
capture = cam.piCapture()

'''Each frame/image with CvCapture structure must be queried (captured). 
the 'capture2' variable carries the file (image/video) and the captured 
frame is returned to 'image' variable.'''
image = cv.QueryFrame(capture)

# Display the queried frame 'image'
print 'Displaying first image capture...'
cv.ShowImage('ORIGINAL', image)

''' convert 'image' to greyscale 
cv.CvtColor(src,dst,cv.OPTION) 
src = source (input) image
dst = destination (output) image'''
print 'Converting to Greyscale...'
no_of_bits = 8
channels = 1
w,h = cv.GetSize(image)
grey = cv.CreateImage((w,h),no_of_bits,channels)
cv.CvtColor(image,grey,cv.CV_RGB2GRAY)
cv.ShowImage('Grey',grey) 

# only using greyscale image for image manipulation here on...

''' Smooth the greyscale image 
cv.Smooth(src,dst,smoothtype)
smoothtype = the type of smoothing; CV_MEDIAN - median filter with AxA square aperture. '''
temp = cv.CreateImage((w,h),no_of_bits,channels)
print 'Smoothing greyscale...'
cv.Smooth(grey,temp,cv.CV_MEDIAN)
cv.ShowImage('Smooth', temp)

''' Equalize Histogram of 'grey' 
cv.EqualizeHist(src,dst) '''
cv.EqualizeHist(grey,temp)
print 'Greyscale equalized histogram...'
cv.ShowImage('Equalized Hist', temp)

''' Binary Threshold allows user to specify a cutoff value for pixels between 0 and 255 '''
threshold = 100
maxValue = 255 	 # Used with CV_THRESH_BINARY and CV_THRESH_BINARY_INV
thresholdType = cv.CV_THRESH_BINARY
cv.Threshold(grey,temp,threshold,maxValue,thresholdType)
print 'Displaying Binary Threshold...'
cv.ShowImage('Binary Threshold',temp)

''' Wait til a key is pressed to end the program '''
while True:
	print 'Press any key to continue...'
	if cv.WaitKey() > 0:
		print 'thanks for pressing a key, exiting loop...'
		break

# Close all windows
print 'Destroying All Windows'
cv.DestroyAllWindows()

