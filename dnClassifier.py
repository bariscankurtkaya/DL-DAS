import cv2
import matplotlib.pyplot as plt
import glob
import numpy as np
import time
from sklearn.metrics import confusion_matrix


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

def averageCalculationWithoutZeros(img):
    averageRow = np.true_divide(img.sum(1), (img != 0).sum(1)) #Inside of the sum is representing dimension
    x = np.nanmean(averageRow, axis = 0)
    #print(averageRow, x)
    return x
    
    
def totalImageCalculator(im_list, imgArray):
    tic = time.time()
    differencePhotoCount = 0
    
    for l in range(len(im_list)):
        img = cv2.imread(im_list[l] , cv2.IMREAD_UNCHANGED)
        average = averageCalculationWithNumpy(img)
        if(average > 35 and average < 97 ):
            differencePhotoCount = differencePhotoCount + 1
            imgArray = np.add(imgArray,img)
        
    toc = time.time()
    print(str(differencePhotoCount), "Photos in ", str((toc-tic)), "seconds\n")
    return imgArray, differencePhotoCount;


    
def thresholdTest(im_list, isNight, averagesArray, filterImg, isFilter):
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
    filterImg = cv2.imread(filterImg , cv2.IMREAD_UNCHANGED)

    for l in range(len(im_list)):
        img = cv2.imread(im_list[l] , cv2.IMREAD_UNCHANGED)
        
        #img = img[0:201,500:900]
        #imgAverage = averageCalculation(x,img)
        
        if isFilter:
            img = img.astype(int)
            filterImg = filterImg.astype(int)
            img = np.multiply(img, filterImg)
            imgAverage = averageCalculationWithoutZeros(img)
        else:
            imgAverage = averageCalculationWithNumpy(img)   #Without Filter
        
        averagesArray.append(imgAverage)
        allSum += imgAverage
        
        if not isFilter:
            # Without Filter and averageCalculationWithNumpy function
            imgAverageThreshold = 75
            allAverageThreshold = 100
        else:
            # 1 2 3 4 5 filter---------------------- averageCalculationWithNumpy function
            #imgAverageThreshold = 54
            #allAverageThreshold = 25
            # 1 2 3 4 5 6 7 8 9 filter ------------------- averageCalculationWithNumpy function
            imgAverageThreshold = 186
            allAverageThreshold = 180
            # 1 2 3 4 5 6 7 8 9 filter ------------------- averageCalculationWithoutZeros function
        
        if(isNight == True):
            if(imgAverage > allMax):
                allMax = imgAverage
                maxName = im_list[l]
            if(imgAverage > imgAverageThreshold):
                nightErrorCount = nightErrorCount + 1

        else:
            if(imgAverage < allMin):
                allMin = imgAverage
                minName = im_list[l]
            if(imgAverage < imgAverageThreshold):
                dayErrorCount = dayErrorCount + 1

    
    
    average = allSum/len(im_list)

    print("average: ", average)
    
    if not isNight:
        print("DAY", average >= allAverageThreshold)
        print(l, " , ", minName, " , ", allMin)
        print("dayErrorCount: ", dayErrorCount)

    else:
        print("NIGHT", average < allAverageThreshold)
        print(l, " , ", maxName, " , ", allMax)
        print("nightErrorCount: ", nightErrorCount)
    toc = time.time()
    print(str(len(im_list)), "Photos in ", str((toc-tic)), "seconds\n")
    return averagesArray
    

def histogramGenerator(nightAveragesArray, dayAveragesArray, isFilter):
    if not isFilter:
        plt.hist(nightAveragesArray, bins=255, range=[0,255])
        plt.hist(dayAveragesArray, bins=255, range=[0,255])
    else:
        plt.hist(nightAveragesArray, bins=500, range=[0,500])
        plt.hist(dayAveragesArray, bins=500, range=[0,500])

    plt.show()
    

def averageImgDisplay(nightImageArray, nightImageCount, dayImageArray, dayImageCount):
    nightTotalImgAverage = nightImageArray/ nightImageCount
    dayTotalImgAverage = dayImageArray/ dayImageCount

    nightTotalImgAverage = nightTotalImgAverage.astype(np.uint8)
    dayTotalImgAverage = dayTotalImgAverage.astype(np.uint8)


    cv2.imshow("night",nightTotalImgAverage)
    cv2.imshow("day",dayTotalImgAverage)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return nightTotalImgAverage, dayTotalImgAverage
    

def saveArrayAsImage(name, array):
    cv2.imwrite(name, array)
    

def readyAverageData():
    dayData = np.load('./Test_results/dayTotalImgAverage.npy')
    nightData = np.load('./Test_results/nightTotalImgAverage.npy')
    return dayData, nightData;
    

def displayImages(nightTotalImgAverage, dayTotalImgAverage):
    nightTotalImgAverage = nightTotalImgAverage.astype(np.uint8)
    dayTotalImgAverage = dayTotalImgAverage.astype(np.uint8)
    
    saveArrayAsImage("./Test_results/nightAverage.png",nightTotalImgAverage)
    saveArrayAsImage("./Test_results/dayAverage.png",dayTotalImgAverage)
    
    cv2.imshow("night",nightTotalImgAverage)
    cv2.imshow("day",dayTotalImgAverage)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

######################### ALGORITHM ##########################

#For MacOs
# im_list_array = ["../../../../Volumes/Bariscan/Dataset/Gece/1/stereo/centre", "../../../../Volumes/Bariscan/Dataset/sample/stereo/centre", "../../../../Volumes/Bariscan/Dataset/gunduz1/Centre"]
im_list_array = ["./Dataset/Gece/1/stereo/centre", "./Dataset/Gece3/1/stereo/centre", "./Dataset/Gece4/1/stereo/centre", "./Dataset/gunduz2/1/stereo/centre", "./Dataset/gunduz3/1/stereo/centre", "./Dataset/gunduz4/1/stereo/centre"]

filterImg = (glob.glob("./Test_results/filterImgNine.png")) 

nightAveragesArray = []
dayAveragesArray = []


nightImageArray = np.array([0]) #It will keep all photographs average pixel by pixel
dayImageArray = np.array([0])


nightImageCount = 0
dayImageCount = 0


isDisplay = True
isDataReady = False
isFilter = False

if not isDataReady:
    for i in range(len(im_list_array)):
        im_list = load_dataset(im_list_array[i])
        
        if "Gece" in im_list_array[i]:
            isNight = True
            
            if not isDisplay:
                nightImageCount += len(im_list)
                averagesArray = thresholdTest(im_list, isNight, nightAveragesArray, filterImg[0], isFilter)
                nightAveragesArray += averagesArray
                
            else:
                nightImageArray, differencePhotoCount = totalImageCalculator(im_list, nightImageArray)
                nightImageCount += differencePhotoCount

        else:
            isNight = False
            
            if not isDisplay:
                dayImageCount += len(im_list)
                averagesArray = thresholdTest(im_list, isNight, dayAveragesArray, filterImg[0], isFilter)
                dayAveragesArray += averagesArray
                
            else:
                dayImageArray, differencePhotoCount = totalImageCalculator(im_list, dayImageArray)
                dayImageCount += differencePhotoCount
            
            
    
    if not isDisplay:
        histogramGenerator(nightAveragesArray, dayAveragesArray, isFilter)
    else:
        nightTotalImgAverage, dayTotalImgAverage = averageImgDisplay(nightImageArray, nightImageCount, dayImageArray, dayImageCount)

else:
    
    dayTotalImgAverage, nightTotalImgAverage = readyAverageData()
    displayImages(nightTotalImgAverage, dayTotalImgAverage)


saveArrayAsImage("differenceNightAverage.png", nightTotalImgAverage)
saveArrayAsImage("differenceDayAverage.png", dayTotalImgAverage)