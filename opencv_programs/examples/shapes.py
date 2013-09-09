#!/usr/bin/python
# Jeremy Barr
# 5/1/2013
# tutorial program using OpenCV Python
# Displays a line, rectangle and circle on the image captured from the camera

import cv #Import functions from OpenCV

capture=cv.CaptureFromCAM(0)
image = cv.QueryFrame(capture)
print "Image Captured"

# points
(x,y) = 1,1
(x2,y2) = 400,400

print "Writing Shapes on Image..."
# Shapes: Line, Rectangle, Circle on 'image' (order matters)
cv.Circle(image,(x+100,y+350),25,(255,255,0),-1,8,0)
cv.Line(image,(x,y),(x2,y2),(0,255,0),4,8)
cv.Rectangle(image,(x+20,y),(x2+50,y2),(0,0,255),1,0)

print "Displaying Image with shapes..."
cv.ShowImage('Shapes',image)
cv.WaitKey(10000)
