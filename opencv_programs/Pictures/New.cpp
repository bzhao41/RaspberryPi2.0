

#include </usr/include/opencv/cv.h>
#include </usr/include/opencv/highgui.h>


int lowerH = 0;
int lowerS = 0;
int lowerV = 0;

int upperH = 0;
int upperS = 0;
int upperV = 0;

IplImage* GetThreshold(IplImage* imgHsv){
  IplImage* imgThresh = cvCreateImage(cvGetSize(imgHsv),IPL_DEPTH_8U, 1);
  cvInRangeS(imgHsv,cvScalar(lowerH,lowerS,lowerV),cvScalar(upperH,upperS,upperV), imgThresh);

  return imgThresh;
}

void setWindow(){

  cvNamedWindow("img");
  cvCreateTrackbar("LowerH", "img", &lowerH, 180, NULL);
  cvCreateTrackbar("UpperH", "img", &upperH, 180, NULL);
  cvCreateTrackbar("LowerS", "img", &lowerS, 256, NULL);
  cvCreateTrackbar("UpperS", "img", &upperS, 256, NULL);
  cvCreateTrackbar("LowerV", "img", &lowerV, 256, NULL);
  cvCreateTrackbar("UpperV", "img", &upperV, 256, NULL);

}

int main(){
  IplImage* img = cvLoadImage("test.png", 1);
  setWindow();
  
  IplImage* imgHsv = cvCreateImage(cvGetSize(img),IPL_DEPTH_8U, 3);
  cvCvtColor(img, imgHsv, CV_BGR2HSV);
  IplImage* imgThresh = GetThreshold(imgHsv);
  cvShowImage("Img", imgThresh);

  cvReleaseImage(&imgHsv);
  cvReleaseImage(&imgThresh);
  cvReleaseImage(&img);

  int c = cvWaitKey(20000);

  return 0;
}
