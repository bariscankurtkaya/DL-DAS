import cv2
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


def totalImageCalculator(im_list, imgArray):
    tic = time.time()
    
    for l in range(len(im_list)):
        img = cv2.imread(im_list[l] , cv2.IMREAD_UNCHANGED)
        imgArray = np.add(imgArray,img)
        
    toc = time.time()
    print(str(len(im_list)), "Photos in ", str((toc-tic)), "seconds\n")
    return imgArray;




def thresholdTest(im_list, isNight, averagesArray):
    #x= 0
    allSum = 0
    average = 0
    allMax = 0
    maxName = ""
    allMin = 255
    minName = ""
    dayErrorCount = 0    
    nightErrorCount = 0
        
    tic = time.time()

    for l in range(len(im_list)):
        img = cv2.imread(im_list[l] , cv2.IMREAD_UNCHANGED)
        
        #img = img[0:201,500:900]
        #imgAverage = averageCalculation(x,img)
        
        imgAverage = averageCalculationWithNumpy(img)
        averagesArray.append(imgAverage)
        allSum += imgAverage
        
        
        if(isNight == True):
            if(imgAverage > allMax):
                allMax = imgAverage
                maxName = im_list[l]
            if(imgAverage > 75):
                nightErrorCount = nightErrorCount + 1

        else:
            if(imgAverage < allMin):
                allMin = imgAverage
                minName = im_list[l]
            if(imgAverage < 75):
                dayErrorCount = dayErrorCount + 1

    
    
    average = allSum/len(im_list)

    print("average: ", average)
    
    if(average >= 100):
        print("DAY")
        print(l, " , ", minName, " , ", allMin)
        print("dayErrorCount: ", dayErrorCount)

    else:
        print("NIGHT")
        print(l, " , ", maxName, " , ", allMax)
        print("nightErrorCount: ", nightErrorCount)
    toc = time.time()
    print(str(len(im_list)), "Photos in ", str((toc-tic)), "seconds\n")
    return averagesArray;
    

def histogramGenerator(nightAveragesArray, dayAveragesArray):
    plt.hist(nightAveragesArray, bins=255, range=[0,255])
    plt.hist(dayAveragesArray, bins=255, range=[0,255])

    plt.show()
    

def averageImgDisplay(nightImageArray, nightImageCount, dayImageArray, dayImageCount):
    nightTotalImgAverage = nightImageArray/ nightImageCount
    dayTotalImgAverage = dayImageArray/ dayImageCount

    nightTotalImgAverage = nightTotalImgAverage.astype(int)
    dayTotalImgAverage = dayTotalImgAverage.astype(int)


    cv2.imshow("night",nightTotalImgAverage)
    cv2.imshow("day",dayTotalImgAverage)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return nightTotalImgAverage, dayTotalImgAverage
    
######################### ALGORITHM ##########################

#For MacOs
# im_list_array = ["../../../../Volumes/Bariscan/Dataset/Gece/1/stereo/centre", "../../../../Volumes/Bariscan/Dataset/sample/stereo/centre", "../../../../Volumes/Bariscan/Dataset/gunduz1/Centre"]
im_list_array = ["./Dataset/Gece/1/stereo/centre", "./Dataset/Gece3/1/stereo/centre", "./Dataset/Gece4/1/stereo/centre", "./Dataset/gunduz2/1/stereo/centre", "./Dataset/gunduz3/1/stereo/centre", "./Dataset/gunduz4/1/stereo/centre"]


nightAveragesArray = []
dayAveragesArray = []


nightImageArray = np.array([0]) #It will keep all photographs average pixel by pixel
dayImageArray = np.array([0])


nightImageCount = 0
dayImageCount = 0


isDisplay = True


for i in range(len(im_list_array)):
    im_list = load_dataset(im_list_array[i])
    
    if "Gece" in im_list_array[i]:
        isNight = True
        nightImageCount += len(im_list)
        
        if not isDisplay:
            averagesArray = thresholdTest(im_list, isNight, nightAveragesArray)
            nightAveragesArray += averagesArray
            
        else:
            nightImageArray = totalImageCalculator(im_list, nightImageArray)
            
    else:
        isNight = False
        dayImageCount += len(im_list)
        
        if not isDisplay:
            averagesArray = thresholdTest(im_list, isNight, dayAveragesArray)
            dayAveragesArray += averagesArray
            
        else:
            dayImageArray = totalImageCalculator(im_list, dayImageArray)

        
        

if not isDisplay:
    histogramGenerator(nightAveragesArray, dayAveragesArray)
else:
    nightTotalImgAverage, dayTotalImgAverage = averageImgDisplay(nightImageArray, nightImageCount, dayImageArray, dayImageCount)
