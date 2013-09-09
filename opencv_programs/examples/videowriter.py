#!/usr/bin/python
# Jeremy barr
# 5/1/2013
# tutorial program using OpenCV Python
# Creates a video from the images captured from the camera

import cv
capture=cv.CaptureFromCAM(0)

fps = 15   # Frames per second
codec = 0  # 0 - uncompressed
image = cv.QueryFrame(capture)

# initialize video writer
writer = cv.CreateVideoWriter("output.avi",codec,fps,cv.GetSize(image),1)

count = 0
while count < 250:
	image = cv.QueryFrame(capture)
	cv.WriteFrame(writer, image)
	cv.ShowImage('Image_Window', image)
	cv.WaitKey(2) # waits 2 milliseconds to move to next frame
	count += 1

