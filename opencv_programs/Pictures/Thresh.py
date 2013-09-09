#!/usr/bin/python


import cv

lowerH = 0
lowerS = 0
lowerV = 0

upperH = 0
upperS = 0
upperV = 0

def getThresholdImage(imgHSV):
    imgThresh = cv.CreateImage(cv.GetSize(imgHSV), IPL_DEPTH_8U, 1)
    cv.InRangeS(imgHSV, cv.Scalar(lowerH,lowerS,lowerV), cv.Scalar(upperH,upperS,UpperV), imgThresh)

    return imgThresh

def setWindows():
    cv.NamedWindow("Image")

    cv.CreateTrackbar("LowerH", "Image", lowerH, 180,None)
    cv.CreateTrackbar("UpperH", "Image", upperH, 180,None)
    cv.CreateTrackbar("LowerS", "Image", lowerS, 256,None)
    cv.CreateTrackbar("UpperS", "Image", upperS, 256,None)
    cv.CreateTrackbar("LowerV", "Image", lowerV, 256,None)
    cv.CreateTrackbar("UpperV", "Image", upperV, 256,None)
    

if __name__=="__main__":

    setWindows()
    img = cv.LoadImage("test.png")
    imgHSV = cv.CreateImage(cv.Getsize(img),IPL_DEPTH_8U, 3)
    cv.CvtColor(img, imgHSV, CV_BGR2HSV)
    
    imgThresh = getThresholdImage(imgHSV)
    cv.ShowImage("img", imgThresh)
