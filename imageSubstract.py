import glob
import numpy as np
import cv2

dayAveragePhoto = (glob.glob("./Test_results/dayAverage.png")) 
nightAveragePhoto = (glob.glob("./Test_results/nightAverage.png")) 

dayImg = cv2.imread(dayAveragePhoto[0] , cv2.IMREAD_UNCHANGED)
nightImg = cv2.imread(nightAveragePhoto[0] , cv2.IMREAD_UNCHANGED)

daySubstractNightImg = dayImg - nightImg
#nightSubstractDayImg = dayImg - nightImg


absoluteDaytoNightImg = np.abs(daySubstractNightImg)
#absoluteNightToDayImg = np.abs(nightSubstractDayImg)


cv2.imwrite("./Test_results/daySubstractNight.png", absoluteDaytoNightImg)
#cv2.imwrite("./Test_results/nightSubstractDay.png", absoluteNightToDayImg)

# Two of them is the same due to absolute function