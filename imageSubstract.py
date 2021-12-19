import glob
import numpy as np
import cv2

################# FUNCTIONS ################


def imageSubstraction(dayImg, nightImg):
    daySubstractNightImg = dayImg - nightImg
    nightSubstractDayImg = nightImg - dayImg


    absoluteDaytoNightImg = np.abs(daySubstractNightImg)
    absoluteNightToDayImg = np.abs(nightSubstractDayImg)

    if(np.array_equal(nightSubstractDayImg, absoluteNightToDayImg)):
        print("same1")
        
    if(np.array_equal(daySubstractNightImg, absoluteDaytoNightImg)):
        print("same2")


    cv2.imwrite("./Test_results/daySubstractNight.png", daySubstractNightImg)
    cv2.imwrite("./Test_results/nightSubstractDay.png", nightSubstractDayImg)


def createFilter(dayImg, nightImg):
    dayFilter = np.zeros((len(dayImg),len(dayImg[0])), dtype = type(dayImg[0][0]))
    nightFilter = np.zeros((len(dayImg),len(dayImg[0])), dtype = type(dayImg[0][0]))

    for i in range(len(dayImg)):
        for j in range(len(dayImg[i])):
            if(int(dayImg[i][j]) - int(nightImg[i][j]) > 127):
                dayFilter[i][j] = dayImg[i][j] - nightImg[i][j]
            elif(int(nightImg[i][j]) - int(dayImg[i][j]) > 127):
                nightFilter[i][j] = nightImg[i][j] - dayImg[i][j]
            
    
    cv2.imwrite("./Test_results/dayFilter.png", dayFilter)
    cv2.imwrite("./Test_results/nightFilter.png", nightFilter)

    
    
    
    
    
################# ALGORITHM ################
dayAveragePhoto = (glob.glob("./Test_results/dayAverage.png")) 
nightAveragePhoto = (glob.glob("./Test_results/nightAverage.png")) 

dayImg = cv2.imread(dayAveragePhoto[0] , cv2.IMREAD_UNCHANGED)
nightImg = cv2.imread(nightAveragePhoto[0] , cv2.IMREAD_UNCHANGED)

#imageSubstraction(dayImg, nightImg)
createFilter(dayImg, nightImg)