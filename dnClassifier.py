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


def averageCalculationWithNumpy(img):
    averageRow = np.average(img, axis=1)
    x = np.average(averageRow)
    #print(x)
    return x

def main(im_listLocation, isNight):
    #x= 0
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

    
    tic = time.time()
    im_list = load_dataset(im_listLocation)
    for l in range(len(im_list)):
        img = cv2.imread(im_list[l] , cv2.IMREAD_UNCHANGED)
        #imgAverage = averageCalculation(x,img)
        imgAverage = averageCalculationWithNumpy(img)
        averagesArray.append(imgAverage)
        allSum += imgAverage
        
        if(isNight == True):
            if(imgAverage > allMax):
                allMax = imgAverage
                maxName = im_list[l]
            if(imgAverage > 95):
                bigOnes = bigOnes + 1
            if(imgAverage > 90):
                lessBiggerOnes = lessBiggerOnes + 1
        else:
            if(imgAverage < allMin):
                allMin = imgAverage
                minName = im_list[l]
            if(imgAverage < 95):
                littleOnes = littleOnes + 1
            if(imgAverage < 100):
                lessOnes = lessOnes + 1
    
    
    average = allSum/len(im_list)

    print("average: ", average)
    
    if(average >= 100):
        print("DAY")
        print(l, " , ", minName, " , ", allMin)
        print("lessOnes: ", lessOnes, " -- littleOnes: ", littleOnes )

    else:
        print("NIGHT")
        print(l, " , ", maxName, " , ", allMax)
        print("lessBiggerOnes: ", lessBiggerOnes, " -- bigOnes: ", bigOnes )

    plt.hist(averagesArray, bins=255, range=[0,255])
    
    toc = time.time()
    print(str(len(im_list)), "Photos in ", str((toc-tic)), "seconds\n")
    
######################### ALGORITHM ##########################

#For MacOs
#im_list = load_dataset("../../../../Volumes/Bariscan/Dataset/Gece/1/stereo/centre")
#im_list = load_dataset("../../../../Volumes/Bariscan/Dataset/sample/stereo/centre")
#im_list = load_dataset("../../../../Volumes/Bariscan/Dataset/gunduz1/Centre")


im_list_array = ["./Dataset/Gece/1/stereo/centre", "./Dataset/Gece3/1/stereo/centre", "./Dataset/gunduz1/centre", "./Dataset/sample/stereo/centre", "./Dataset/gunduz2/1/stereo/centre", "./Dataset/gunduz3/1/stereo/centre"]

for i in range(len(im_list_array)):
    if "Gece" in im_list_array[i]:
        isNight = True
    else:
        isNight = False

    main(im_list_array[i], isNight)




plt.show()


#cv2.waitKey(0)
#cv2.destroyAllWindows()