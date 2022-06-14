import cv2
import numpy as np
import glob

location = "/Volumes/Barışcan HDD/tubitak-2209/Dataset/Gece3/1/stereo/centre/*"
img = (glob.glob("/Volumes/Barışcan HDD/tubitak-2209/Dataset/1418236403008951.png"))[0]
img = cv2.imread(img, cv2.IMREAD_UNCHANGED)
frameSize = (img.shape[1], img.shape[0])

out = cv2.VideoWriter('output_video.avi',cv2.VideoWriter_fourcc(*'DIVX'), 16, frameSize)

for filename in glob.glob(location):
    img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    out.write(img)

out.release()

