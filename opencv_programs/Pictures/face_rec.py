import cv2
from subprocess import call

#call(["sudo raspistill -t 0 -h 324 -w 432 -o /home/pi/opencv_programs/Pictures/picture.jpg"], shell = True)

img = cv2.imread("/home/pi/opencv_programs/Pictures/blob_11.png")
cascade = cv2.CascadeClassifier("/home/pi/opencv_programs/Pictures/haarcascade_frontalface_alt.xml")
rects = cascade.detectMultiScale(img,1.3,4,cv2.cv.CV_HAAR_SCALE_IMAGE,(20,20))
if len(rects) == 0:
    rects = []
rects[:, 2:] += rects[:,:2]

for x1,y1,x2,y2 in rects:
    cv2.rectangle(img, (x1,y1),(x2,y2), (127,255,0), 2)
cv2.imwrite("/home/pi/opencv_programs/Pictures/detected.jpg",img)
