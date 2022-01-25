import cv2 #pip install opencv-python
import numpy

myimg = cv2.imread("Metadata/cover.png")
avg_color_per_row = numpy.average(myimg, axis=0)
avg_color = numpy.average(avg_color_per_row, axis=0)
red = avg_color[2]
green = avg_color[1]
blue = avg_color[0]
print("Red " + str(red))
print("Green " + str(green))
print("Blue " + str(blue))