import cv2 as cv
import numpy as np
from tqdm import tqdm
from glob import glob


main_dataset_dir = '/data/scratch/bariskurtkaya/oxford'
datasets = glob(main_dataset_dir + '/*')

hist = np.zeros((7,256))

for idx, data_dir in enumerate(datasets):
    for _, data in tqdm(enumerate(glob(data_dir + '/stereo/centre/*'))):
        img = cv.imread(data, 0)
                
        hist[idx] = np.add(hist[idx], np.histogram(img, bins=256, range=(0,256))[0])


with open('histograms.npy', 'wb') as f:
    np.save(f, hist)