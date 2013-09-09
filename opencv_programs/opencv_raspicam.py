'''
@author Jeremy Barr
@date 5/20/2013
@brief Example script integrates OpenCV and the RaspiCam.py class
'''

from raspicam import RaspiCam
import cv

# initialize raspPi cam modue class
rCam = RaspiCam()

rPic = rCam.piCapture()

# not displaying image. Check class code
cv.ShowImage("RasPiCam",rPic)

cv.WaitKey(10000)

