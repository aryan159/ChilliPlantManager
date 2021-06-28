import cv2 as cv
import numpy as np
import sys

img = cv.imread(cv.samples.findFile("ChilliPlantCropped.jpeg"))
if img is None:
    sys.exit("Could not read the image.")
 
img = cv.resize(img, (723,700))
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

cv.imshow("original", img)
k = cv.waitKey(0)

zeroes = np.zeros((700,723))
hsv[:,:,2] = zeroes
editedImg = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)

cv.imshow("edited", editedImg)
k = cv.waitKey(0)

