import os
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import glob
import numpy as np
import time

def load_dataset(image_dir):
    return (glob.glob(image_dir + "/*.png")) 


def averageCalculation(x, img):
    for i in range(len(img)):
        for j in range(len(img[i])):
            x += img[i][j]
            
    imageShape = (img.shape[0]*img.shape[1])
    x = x/imageShape
    return x


def averageCalculationWithNumpy(x,img):
    averageColumn = np.average(img, axis=1)
    x = np.average(averageColumn)
    print(x)
    return x


######################### ALGORITHM ##########################

x= 0
allSum = 0
average = 0
allMax = 0
maxName = ""
allMin = 255
minName = ""
littleOnes = 0
lessOnes = 0
bigOnes = 0
lessBiggerOnes = 0
averagesArray = []

#### Night ####

im_list = load_dataset("./Dataset/Gece/1/stereo/centre")

#For MacOs
#im_list = load_dataset("../../../../Volumes/Bariscan/Dataset/Gece/1/stereo/centre")

tic = time.time()

for l in range(len(im_list)):
    img = cv2.imread(im_list[l] , cv2.IMREAD_UNCHANGED)
    #imgAverage = averageCalculation(x,img)
    imgAverage = averageCalculationWithNumpy(x,img)
    averagesArray.append(imgAverage)
    allSum += imgAverage
    if(imgAverage > allMax):
        allMax = imgAverage
        maxName = im_list[l]
        print(l , " , " , maxName , " , " , allMax)
    if(imgAverage > 100):
        bigOnes = bigOnes + 1
    if(imgAverage > 95):
        lessBiggerOnes = lessBiggerOnes + 1
    print("lessBiggerOnes: ", lessBiggerOnes, " -- bigOnes: ", bigOnes )


"""
#### Day ####

#im_list = load_dataset("./Dataset/gunduz1/centre")

#im_list = load_dataset("./Dataset/sample/stereo/centre")

#For my MacOs
im_list = load_dataset("../../../../Volumes/Bariscan/Dataset/sample/stereo/centre")
im_list = load_dataset("../../../../Volumes/Bariscan/Dataset/gunduz1/Centre")



for l in range(len(im_list)):
    img = cv2.imread(im_list[l] , cv2.IMREAD_UNCHANGED)
    #imgAverage = averageCalculation(x,img)
    imgAverage = averageCalculationWithNumpy(x,img)
    allSum += imgAverage
    if(imgAverage < allMin):
        allMin = imgAverage
        minName = im_list[l]
        print(l , " , " , minName , " , " , allMin)
    if(imgAverage < 100):
        littleOnes = littleOnes + 1
    if(imgAverage < 105):
        lessOnes = lessOnes + 1
    print("lessOnes: ", lessOnes, " -- littleOnes: ", littleOnes )
"""

toc = time.time()
average = allSum/len(im_list)

print("average: ", average)

if(average >= 100):
    print("day")
    print(l, " , ", minName, " , ", allMin)
else:
    print("night")
    print(l, " , ", maxName, " , ", allMax)

print(str(len(im_list)), "Photos in ", str((toc-tic)), "seconds")

plt.hist(averagesArray, bins=100)
plt.show()


#cv2.waitKey(0)
#cv2.destroyAllWindows()