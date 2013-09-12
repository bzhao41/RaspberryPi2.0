#!/usr/bin/python

'''
@author Bruce Zhao
'''

import cv
import cvblob
import copy
import math
import time
import zbar
import Image
import socket
from subprocess import call

#Finds blobs in HSV range. Main function for finding blobs
def findBlobs(img, min_color, max_color, originalwindow, renderedwindow, location, area, ratio):
    blobs = cvblob.Blobs() #creates a dictionary of blobs
    size = cv.GetSize(img) #gets size of image

    hsv = cv.CreateImage(size, cv.IPL_DEPTH_8U, 3) #New HSV image for alter
    thresh = cv.CreateImage(size, cv.IPL_DEPTH_8U,1) #New Gray Image for later
    labelImg = cv.CreateImage(size, cvblob.IPL_DEPTH_LABEL, 1) #New Blob image for later

    cv.CvtColor(img,hsv,cv.CV_BGR2HSV) #converts image to hsv image
    cv.InRangeS(hsv, min_color, max_color, thresh) #thresholds it
    
    #Corrections to remove false positives
    cv.Smooth(thresh, thresh, cv.CV_BLUR)
    cv.Dilate(thresh, thresh)
    cv.Erode(thresh, thresh)

    result = cvblob.Label(thresh, labelImg, blobs) #extracts blobs from a greyscale image
    
    numblobs = len(blobs.keys()) #number of blobs based off of length of blobs dictionary
    
    #if there are blobs found
    if (numblobs > 0):
        avgsize = int(result / numblobs) 
        print str(numblobs) + " blobs found covering " + str(result) + "px"   
        
        #Removes blobs that are smaller than a certain size based off of average size
        remv = []
        for x in blobs:
            if (blobs[x].area < avgsize/ratio):
                remv.append(x)
        for x in remv:
            del blobs[x]
        
        numblobs = len(blobs.keys()) #gets the number of blobs again after removing some
        print str(numblobs) + " blobs remaining"           

        filtered = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 1) 
        cvblob.FilterLabels(labelImg, filtered, blobs) #Creates a binary image with the blobs formed (imgIn, imgOut, blobs)
        
        #Centroid, area, and circle for all blobs
        for blob in blobs:
            location.append(cvblob.Centroid(blobs[blob]))
            area.append(blobs[blob].area)
            cv.Circle(img,(int(cvblob.Centroid(blobs[blob])[0]),int(cvblob.Centroid(blobs[blob])[1])), int(math.sqrt(int(blobs[blob].area)/3.14))+ 25, cv.Scalar(0,0,0))

        imgOut = cv.CreateImage(cv.GetSize(img), cv.IPL_DEPTH_8U, 3)
        cv.Zero(imgOut)

        cvblob.RenderBlobs(labelImg, blobs, img, imgOut, cvblob.CV_BLOB_RENDER_COLOR|cvblob.CV_BLOB_RENDER_CENTROID|cvblob.CV_BLOB_RENDER_BOUNDING_BOX|cvblob.CV_BLOB_RENDER_ANGLE, 1.0) #Marks up the blobs image to put bounding boxes, etc on it
        cv.ResizeWindow("Window", 640,480)
        cv.ResizeWindow("Rendered",640,480)
        cv.ShowImage("Window" , img) #shows the orininalimage
        cv.ShowImage("Rendered", imgOut) #shows the blobs image

        return blobs #returns the list of blobs
 
    else:
        print " ...Zero blobs found. \nRedifine color range for better results" #if no blobs were found print an error message
        cv.ResizeWindow("Window", 640,480)
        cv.ResizeWindow("Rendered",640,480)
        cv.ShowImage("Window", img) #show the original image
    
#Find blobs based off of RGB values instead. The RGB is converted into HSV. Location and area are arrays
def findRGBBlobs(img, color, originalwindow, renderedwindow, location, area, ratio, bounds):
    R = int(color[0]) 
    G = int(color[1])
    B = int(color[2])
    if (R == G) & (G == B):   #This is to make sure that all three values aren't equal because then we get a divide by zero error
        if (R <= 253):
            G = R + 1
            B = R + 2
        elif (R > 253):
            G = R - 1
            B = R - 2
    #gets the biggest color
    if (R >= G) & (R >= B):  
        maxc= R
    elif (G >= R) & (G >= B):
        maxc= G
    else:
        maxc= B
    #gets the smallest color
    if (R <= G) & (R <= B):
        minc= R
    elif (G <= R) & (G <= B):
        minc= G
    else: 
        minc= B

    #gets the difference between the max and min colors
    delta = (maxc - minc)

    #finds the H value based off of what the max color was. OpenCV is weird on hsv because the H value is from 0-180 instead of 0-360. The V and S values use the full 8 bit range so they go from 0-255 instead of 0-1.
    if (maxc == R):
        H = (G - B)/ delta * 30
    elif (maxc == B):
        H = (((R - G)/delta) + 4) * 30
    else:
        H = (((B - R)/delta) + 2) * 30
    
    if (H < 0):
        H = H + 180
    elif ( H > 180):
        H = H - 180

    S = int(delta * 255/maxc + .5)

    V = int(maxc + .5)

    #finds a suitable min and max range. bounds can be changed to find larger or smaller ranges and if the numbers are lower than 0 or larger than the max for each value, they are set to either 0 or the max value.
    
    minh = H - bounds
    if (minh < 0):
        minh = 0
    maxh = H + bounds
    if (maxh > 180):
        maxh = 180
    mins = S - bounds
    if (mins < 0):
        mins = 0
    maxs = S + bounds
    if (maxs > 255):
        maxs = 255
    minv = V - bounds
    if (minv < 0):
        minv = 0
    maxv = V + bounds
    if (maxv > 255):
        maxv = 255

    return findBlobs(img, cv.Scalar(minh,mins,minv),cv.Scalar(maxh,maxs,maxv), originalwindow,renderedwindow,location, area, ratio)

#finds QR codes in an image using zbar library
def findQRcodes(img):
   grayimage = cv.CreateImage(cv.GetSize(img), img.depth, 1) #We have to create a greyscale copy of the original image for zbar to work
   cv.CvtColor(img, grayimage, cv.CV_RGB2GRAY)
   width = grayimage.width
   height = grayimage.height
   raw = grayimage.tostring()
   zimage = zbar.Image(width, height, 'Y800', raw) #a zbar image type to find qr codes. Some people say that you need PIL but opencv is just fine at converting images to strings. Some people will say use LoadImageM but LoadImage works too as it also has a tostring method.
   scanner = zbar.ImageScanner() #new instance of a scanner
   scanner.parse_config('enable') #enables the scanner I guess
   scanner.scan(zimage) #scans the image
   #does stuff to the symbols found
   #for symbol in zimage:
   #    print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
   for symbol in zimage: #Goes through scanned symbols
       if symbol != None: #If the symbol exists
           return str(symbol.type) + " " + str(symbol.data) # return the symbol
       else: 
           return None

#Combination of previous functions to find qr codes based off of blob locations.
def qrBlobs(img, color, window, rendered, ratio = 1, bounds = 20):
    location = [] 
    area = []
    blobs  = findRGBBlobs(img, color, window, rendered, location, area, ratio, bounds)
    if blobs!=None:
        for blob in blobs:
            print(str(findQRcodes(resize(cropImage(img, (blobs[blob].minx, blobs[blob].miny, blobs[blob].maxx - blobs[blob].minx, blobs[blob].maxy - blobs[blob].miny)), 640, 480))))
        return dict(zip(location,area)) #returns a dictionary of centroids and the area of the blobs at the centroid
    else:
        return "Nothing to be found"
    
#I don't know if we'll need to finish this if qr codes do work.
def trackBlobsRGB(color, window, rendered):
    #overwrite one image over and over again
    location = []
    area = []
    while True:
        start = time.time()
        call(["sudo raspistill -t 0 -h 324 -w 432 -o /home/pi/opencv_programs/Pictures/output.jpg"], shell = True)
        img = LoadImage("output.jpg", 1)
        findRGBBlobs(img, color, window, rendered, location, area)
        if(len(location) > 1):  
            print str(distance(location[len(location) - 2], location[len(location) - 1]))
    #Save pictures in seperate files
    #imageName = "/home/pi/opencv_programs/Pictures/image" +str(a) + ".jpg"
    #call(["sudo raspistill -n -q 10 -t 0 -h 324 -w 432 -o " + imageName], shell = True)

#wait for the esc key to be pressed
def waitESC():
    k = cv.WaitKey()
    while k!=27:
           k = cv.WaitKey(33)

#resizes an image
def resize(img, width, height):
    smallImage = cv.CreateImage((height,width), img.depth, img.nChannels)
    cv.Resize(img,smallImage,interpolation = cv.CV_INTER_NN)
    return smallImage

def multiResize(img, widthlim, heightlim, times):
    if (widthlim / img.width * img.height > heightlim):
        maxheight = heightlim
        maxwidth = heightlim * img.width / img.height
        
    elif (heightlim / img.height * img.width > widthlim):
        maxwidth = widthlim
        maxheight = widthlim * img.height / img.width 
    else:
        maxwidth = widthlim
        maxheight = heightlim

    widthinter = int((maxwidth - img.width)/times)
    heightinter = int((maxheight - img.height)/times)

    small = resize(img, img.width + widthinter, img.height + heightinter)
    for t in range(2, times + 1):
      small = resize(small, small.width + widthinter, small.height+heightinter)
      cv.Smooth(small, small, cv.CV_BLUR)
    return small
#area should be a tupple (x , y, width, height)
#Crops an image to a specified Range without changing the original image as SetImageROI is wont to do 
def cropImage(img, croparea):
    inbetween = cv.CreateImage(cv.GetSize(img), img.depth, img.nChannels)
    cv.Copy(img, inbetween)
    cv.SetImageROI(inbetween, croparea)
    return inbetween

#finds the distance between two points
def distance(tup1,tup2):
    x1 = int(tup1[0])
    x2 = int(tup2[0])
    y1 = int(tup1[1])
    y2 = int(tup2[1])
    return math.sqrt(math.pow(x2-x1,2) + math.pow(y2-y1,2))

if __name__=="__main__":
    
    
    #This creates empty windows so taht instead of having to create windows for images that are shown, they
    #are shown here and the windows just reload everytime a new image is shown
    a = cv.NamedWindow("Window", cv.CV_WINDOW_NORMAL)
    b = cv.NamedWindow("Rendered" , cv.CV_WINDOW_NORMAL)
    cv.MoveWindow("Window", 50, 50)
    cv.MoveWindow("Rendered", 690, 50)

    #This call and load piece is for testing out functions with images that the camera takes instead of images that are for testing purposes. The first call is for taking pictures taht are 640 by 480 and the second call is for taking pictures at full resolution, 2592 by 1944 
    #call(["sudo raspistill -n -t 0 -w 640 -h 480  -o /home/pi/opencv_programs/Pictures/output.jpg"], shell = True) #Resolution 640/480
    #call(["sudo raspistill -n -t 0 -o /home/pi/opencv_programs/Pictures/output.jpg"], shell = True) #Full quality/resolution
    #img = cv.LoadImage("output.jpg", 1)
    

    #This piece is for testing outside of the server. findRGBblobs returns a dictionary of locations and areas and is provided two arrays. color is a scalar that represents rgb values right now. 
    location = []
    area = []
    img = cv.LoadImage("test1.png")
    color = cv.Scalar(1,255,255)
    #findRGBBlobs(img4, color, "Window", "Rendered", location, area, 3, 20)
    qrBlobs(img, color, "Window", "Rendered", 3, 20)
    waitESC()

    #Server setup - The host and ports are set for the RPi to bind onto. The server waits to
    #receive information froma  client and when it does receive some sort of information and then it 
    #proceeds to starting a loop and sending a dictionary of locations and their corresponding blob areas
    #host = '158.130.158.227'
    #port = 5001
    #size = 1024
    #backlog = 1
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.bind((host,port))
    #print "bound successful"
    #s.listen(backlog)
    #while 1:
    #    print "Ready"
    #    client, adress = s.accept()
    #    data = client.recv(size)
    #    print str(data)
    #    while data:
    #        call(["sudo raspistill -n -t 0 -w 640 -h 480 -o /home/pi/opencv_programs/Pictures/output.jpg"], shell = True)
    #        img4 = cv.LoadImage("output.jpg", 1)
    #        client.send(str(qrBlobs(img4, color, "Window", "Rendered")))
    #        waitESC()
        

    
#todo: improve rgbfinder
#improve qr finding
#improve multiresizing with erosions and dilations and whatnot to improve the smoothness

#Finished:
#Server is implemented. Can be improved
#Find blobs now finds multiple blobs instead of just the largest blob
#MultiResizing

#TODO:
#Figure out how to resize QR codes better
