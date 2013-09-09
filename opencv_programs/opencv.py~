'''
@author Jeremy Barr
@date 5/1/2013
@brief sample script to test camera with OpenCV
'''

import cv2.cv as cv
import time

cv.NamedWindow("webcam", cv.CV_WINDOW_AUTOSIZE)
capture = cv.CaptureFromCAM(0)

cv.ShowImage("webcam", cv.QueryFrame(capture))

print "Press any key or Wait 5 seconds..."
# pause five seconds
cv.WaitKey(5000)
