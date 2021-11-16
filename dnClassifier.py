import os
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import glob

def load_dataset(image_dir):
    return (glob.glob(image_dir + "/*.png")) 


def avarageCalculation(x, img):
    for i in range(len(img)):
        for j in range(len(img[i])):
            x += img[i][j]
            
    imageShape = (img.shape[0]*img.shape[1])
    x = x/imageShape
    return x
        




######################### ALGORITHM ##########################

x= 0 
allSum = 0
avarage = 0
allMax = 0
maxName = ""
allMin = 255
minName = ""
littleOnes = 0
lessOnes = 0

#### Night ####
"""
im_list = load_dataset("./Dataset/Gece/1/stereo/centre")

for l in range(len(im_list)):
    img = cv2.imread(im_list[l] , cv2.IMREAD_UNCHANGED)
    imgAvarage = avarageCalculation(x,img)
    allSum += imgAvarage
    if(imgAvarage > allMax):
        allMax = imgAvarage
        maxName = im_list[l]
        print(l , " , " , maxName , " , " , allMax)
"""


#### Day ####

#im_list = load_dataset("./Dataset/Gündüz1/centre")

im_list = load_dataset("./Dataset/sample/stereo/centre")


for l in range(len(im_list)):
    img = cv2.imread(im_list[l] , cv2.IMREAD_UNCHANGED)
    imgAvarage = avarageCalculation(x,img)
    allSum += imgAvarage
    if(imgAvarage < allMin):
        allMin = imgAvarage
        minName = im_list[l]
        print(l , " , " , minName , " , " , allMin)
    if(imgAvarage < 100):
        littleOnes = littleOnes + 1
    if(imgAvarage < 105):
        lessOnes = lessOnes + 1
    print("lessOnes: ", lessOnes, " -- littleOnes: ", littleOnes )



avarage = allSum/len(im_list)

print(avarage)

if(avarage >= 110):
    print("day")
else:
    print("night")
    
    
cv2.waitKey(0)
cv2.destroyAllWindows()