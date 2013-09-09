#!/usr/bin/python/

import cv

a = cv.NamedWindow("window")
img = cv.LoadImage("smlTable1.jpg", 1)
img2 = cv.LoadImage("smlTable2.jpg", 1)
img3 = cv.LoadImage("smlTable3.jpg", 1)
cv.ShowImage("window", img)
cv.WaitKey(1000)
cv.ShowImage("window", img2)
cv.WaitKey(20000)
