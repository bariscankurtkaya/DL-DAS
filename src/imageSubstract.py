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


    cv2.imwrite("../Test_results/dayDifferenceSubstractNight.png", daySubstractNightImg)
    cv2.imwrite("../Test_results/nightDifferenceSubstractDay.png", nightSubstractDayImg)


def createFilter(dayImg, nightImg):
    filterImg = np.zeros((len(dayImg),len(dayImg[0])), dtype = type(dayImg[0][0]))

    filterImg = np.exp((nightImg - dayImg)/16)
    filterImg[filterImg<2.71] = 0
    filterImg = filterImg / np.exp(8) #normalization
     
    #filterImg = np.round(filterImg)
    #filterImg = filterImg.astype(np.uint8)
    #cv2.imwrite("../Test_results/differenceFilterImgGreaterExp.png", filterImg)
    np.savetxt("../Test_results/differenceFilterImgGreaterExp.csv", filterImg, delimiter=',')
    return filterImg
    
    
    
    
    
################# ALGORITHM ################
if __name__ == "__main__":
    dayAveragePhoto = (glob.glob("../Test_results/differenceDayAverage.png")) 
    nightAveragePhoto = (glob.glob("../Test_results/differenceNightAverage.png")) 

    dayImg = cv2.imread(dayAveragePhoto[0] , cv2.IMREAD_UNCHANGED)
    nightImg = cv2.imread(nightAveragePhoto[0] , cv2.IMREAD_UNCHANGED)

    #imageSubstraction(dayImg, nightImg)
    filterImg = createFilter(dayImg, nightImg)

