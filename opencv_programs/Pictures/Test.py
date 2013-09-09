#!/usr/bin/env python

import os
from subprocess import call
import cv2.cv as cv
import time

#call(["sudo raspistill -t 0 -h 324 -w 432 -o /home/pi/opencv_programs/Pictures/output.jpg"], shell = True)

cv.NamedWindow('a', 1)

cam = cv.CaptureFromCAM(-1)
cv.SetCaptureProperty(cam, cv.CV_CAP_PROP_FRAME_HEIGHT, 324)
cv.SetCaptureProperty(cam, cv.CV_CAP_PROP_FRAME_WIDTH, 432)

frames = 0
start_time = time.time()
while True:
    frame = cv.QueryFrame(cam)
    cv.ShowImage('a', frame)

    c = cv.WaitKey(50)
    if c == 27:
        exit(0)
    
    print "Frames", frames
    frames += 1

    if frames % 10 == 0:
        currtime = time.time()
        numsecs = currtime - start_time
        fps = frames/numsecs
        print "FPS: ", fps
