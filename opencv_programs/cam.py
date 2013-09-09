import cv2,cv
import numpy as np

# start capturing images from webcam for video
c = cv2.VideoCapture(0)

print "Press ESC to exit"

while(1):
    # reading from VideoCapture object 'c'
    _,f = c.read()

    # display images
    #cv2.imshow('cv2 stuff',f)
    #frame = cv.fromarray(f)

    # key pressed during the 10ms delay
    key = cv2.waitKey(10)

    # if ESC is pressed then break
    if key == 27:
        break
    # if Enter is pressed then save image captured in current directory
    # jpeg compression. 'cam.jpg' is overwritten if a JPEG of that name already exists.
    elif key == 10:       
        cv.SaveImage('cam.jpg',frame)
        print "Image Saved"
	print "Press ESC to exit..."

# close windows when out of loop
cv2.destroyAllWindows()
print "Windows Destroyed"
