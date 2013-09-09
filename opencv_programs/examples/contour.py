'''
@author Jeremy Barr
@date 5/10/2013
@brief Python Script uses NumPy arrays and OpenCV 'contours' to draw and display shapes as contour lines
The image is composed of a 100x100 array
'''

import numpy as np
import cv2

contours = [np.array([[1,1],[10,50],[50,50]], dtype=np.int32), np.array([[99,99],[99,60],[60,99]], dtype=np.int32)]

drawing = np.zeros([100,100],np.uint8)
for cnt in contours:
	cv2.drawContours(drawing, [cnt],0,(255,255,255),2)

cv2.imshow('output',drawing)
cv2.waitKey(0)
