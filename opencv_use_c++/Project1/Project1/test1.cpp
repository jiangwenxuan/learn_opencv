#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;

int main() {
	Mat img = imread("test1.png");
	imshow("image test", img);
	waitKey(100);
	return 0;
}