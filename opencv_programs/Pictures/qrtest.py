import zbar
import cv

img = cv.LoadImage("qrtest.png", 1)
inbetween = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 3)
cv.Copy(img,inbetween)
cv.SetImageROI(inbetween,(10,10,200,200))

cv.ShowImage("Original", img)
cv.ShowImage("Cropped", inbetween)
cv.WaitKey(200000)
