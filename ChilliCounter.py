import cv2 as cv
import sys
import numpy as np
import math

original_stdout = sys.stdout

def PixelGrouper(img, dist=0.05, size=0.00002):
    """Groups closeby pixels together
    
    (img) -> 2d numpy array with 1s representing the colour we are interested in and 0s representing everything else
    (dist) -> a float distance threshold of the diagonal of the image for whether pixels are in the same group
    (size) -> a float (relative to total number of pixels) threshold for whether a group is a valid chilli
    """
    
    #find nearby pixels within threshold via list of tuples(xModifier, yModifier)
    yMax = int(img.shape[0]*dist)
    xMax = int(img.shape[1]*dist)

    #find minNumOfPixels
    minNumOfPixels = int(size*img.shape[0]*img.shape[1]) + 1
    print("Minimum number of pixels: ", minNumOfPixels)

    modifiers = []
    for x in range(0,xMax+1):
        for y in range(0,yMax+1):

            if x==0 and y==0:
                continue

            modifiers.append(tuple((x, y)))
            if x!=0:
                modifiers.append(tuple((x*-1, y)))
            if y!=0:
                modifiers.append(tuple((x, y*-1)))
            if x!=0 and y!=0:
                modifiers.append(tuple((x*-1, y*-1)))

    currentGroup = 2
    toCheck = []
    numOfPixels = 0
    invalidChillies = 0
    #main loop
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            #find the pixel
            if img[y][x] == 1:
                toCheck.append(tuple((x,y)))
                
                #find and annotate every pixel in group
                while toCheck:
                    currentPixel = toCheck.pop()
                    if img[currentPixel[1], currentPixel[0]] == 1:
                        img[currentPixel[1], currentPixel[0]] = currentGroup
                        numOfPixels += 1
                        for modifier in modifiers:
                            toCheck.append(tuple((x + modifier[0], y + modifier[1])))
                if numOfPixels < minNumOfPixels:
                    invalidChillies += 1
                print("Group ", currentGroup-1, "has ", numOfPixels, " pixels")
                currentGroup += 1
                numOfPixels = 0

    return (currentGroup-2-invalidChillies, currentGroup-2, img)
                        


#import image
img = cv.imread(cv.samples.findFile("photos/ChilliPlantCropped.jpeg"))
if img is None:
    sys.exit("Could not read the image.")

#resize image to 723, 700
img = cv.resize(img, (500,500))

#single out the red pixels
lower = np.array([0, 124, 0])
upper = np.array([12,255,255])

hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv, lower, upper)
output = cv.bitwise_and(img,img, mask= mask)

formattedOutput = cv.cvtColor(output, cv.COLOR_HSV2BGR)[:,:,2]

for row in range(formattedOutput.shape[0]):
    for column in range(formattedOutput.shape[1]):
        if formattedOutput[row][column] > 0:
            formattedOutput[row][column] = 1

(numOfChillies, numOfGroups, groupedOutput) = PixelGrouper(formattedOutput)

print("NO.OF CHILLIES: ", numOfChillies)

cv.imshow("original", output)
k = cv.waitKey(0)

for i in range(2, numOfGroups+2):
    out = np.where(groupedOutput==i, 255, 0)
    output[:,:,2] = out
    display = cv.cvtColor(output, cv.COLOR_HSV2BGR)
    cv.imshow(str(i-1), display)
    k = cv.waitKey(0)














#output unlimited to file
""" with open('output.txt', 'w') as f:
    sys.stdout = f
    with np.printoptions(threshold=np.inf):
        print(redness)
    sys.stdout = original_stdout """

