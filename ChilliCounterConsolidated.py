#Red Chillies ->  s(hMin = 0 , sMin = 124, vMin = 0), (hMax = 12 , sMax = 255, vMax = 255)

import cv2 as cv
import sys
import numpy as np

IMAGE_PATH = 'photos/110421.jpg'

def nothing(x):
    pass

# Load in image
image = cv.imread(IMAGE_PATH)
image = cv.resize(image, (1920,550))

# Create a window
cv.namedWindow('image')

# create trackbars for color change
cv.createTrackbar('HMin','image',0,179,nothing) # Hue is from 0-179 for Opencv
cv.createTrackbar('SMin','image',0,255,nothing)
cv.createTrackbar('VMin','image',0,255,nothing)
cv.createTrackbar('HMax','image',0,179,nothing)
cv.createTrackbar('SMax','image',0,255,nothing)
cv.createTrackbar('VMax','image',0,255,nothing)

# Set default value for MAX HSV trackbars.
cv.setTrackbarPos('HMax', 'image', 179)
cv.setTrackbarPos('SMax', 'image', 255)
cv.setTrackbarPos('VMax', 'image', 255)

# Initialize to check if HSV min/max value changes
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

output = image
wait_time = 33

while(1):

    # get current positions of all trackbars
    hMin = cv.getTrackbarPos('HMin','image')
    sMin = cv.getTrackbarPos('SMin','image')
    vMin = cv.getTrackbarPos('VMin','image')

    hMax = cv.getTrackbarPos('HMax','image')
    sMax = cv.getTrackbarPos('SMax','image')
    vMax = cv.getTrackbarPos('VMax','image')

    # Set minimum and max HSV values to display
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Create HSV Image and threshold into a range.
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower, upper)
    output = cv.bitwise_and(image,image, mask= mask)

    # Print if there is a change in HSV value
    if( (phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
        print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
        phMin = hMin
        psMin = sMin
        pvMin = vMin
        phMax = hMax
        psMax = sMax
        pvMax = vMax

    # Display output image
    cv.imshow('image',output)

    # Wait longer to prevent freeze for videos.
    if cv.waitKey(wait_time) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()

original_stdout = sys.stdout

def PixelGrouper(originalImg, img, dist=0.05, size=0.00002):
    """Groups closeby pixels together

    (originalImg) -> The original Image
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


    annotatedImg = originalImg.copy()
    font = cv.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    color = (255, 255, 255)
    thickness = 1

    #main loop
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            #find the pixel
            if img[y][x] == 1:
                toCheck.append(tuple((x,y)))
                
                #find and annotate every pixel in group
                lowestPixelY = 0
                while toCheck:
                    currentPixel = toCheck.pop()
                    if img[currentPixel[1], currentPixel[0]] == 1:
                        img[currentPixel[1], currentPixel[0]] = currentGroup
                        numOfPixels += 1
                        if currentPixel[1] > lowestPixelY:
                            lowestPixelY = currentPixel[1]
                            lowestPixelX = currentPixel[0]
                        for modifier in modifiers:
                            toCheck.append(tuple((x + modifier[0], y + modifier[1])))
                if numOfPixels < minNumOfPixels:
                    invalidChillies += 1
                else:
                    annotatedImg = cv.putText(annotatedImg, str(currentGroup - 1 - invalidChillies), (lowestPixelX, lowestPixelY+5), font, fontScale, color, thickness, cv.LINE_AA)

                #print("Group ", currentGroup-1, "has ", numOfPixels, " pixels")
                currentGroup += 1
                numOfPixels = 0

    return (currentGroup-2-invalidChillies, currentGroup-2, img, annotatedImg)
                        


#import image
img = cv.imread(cv.samples.findFile(IMAGE_PATH))
if img is None:
    sys.exit("Could not read the image.")

#resize image
img = cv.resize(img, (500,500))

#single out the red pixels
lower = np.array([hMin, sMin, vMin])
upper = np.array([hMax, sMax, vMax])

hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv, lower, upper)
output = cv.bitwise_and(img,img, mask= mask)

formattedOutput = cv.cvtColor(output, cv.COLOR_HSV2BGR)[:,:,2]

for row in range(formattedOutput.shape[0]):
    for column in range(formattedOutput.shape[1]):
        if formattedOutput[row][column] > 0:
            formattedOutput[row][column] = 1

(numOfChillies, numOfGroups, groupedOutput, annotatedImg) = PixelGrouper(img, formattedOutput)

print("NO.OF CHILLIES: ", numOfChillies)

cv.imshow("annotated", annotatedImg)
k = cv.waitKey(0)

# for i in range(2, numOfGroups+2):
#     out = np.where(groupedOutput==i, 255, 0)
#     output[:,:,2] = out
#     display = cv.cvtColor(output, cv.COLOR_HSV2BGR)
#     cv.imshow(str(i-1), display)
#     k = cv.waitKey(0)