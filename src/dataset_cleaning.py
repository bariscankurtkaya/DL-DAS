import os
from glob import glob

dataset_dir = "/data/scratch/bariskurtkaya/oxford/yolo/2014-11-14-16-34-33/stereo/centre/"


txt_files = glob(dataset_dir+ "*.txt")
png_files =  glob(dataset_dir+ "*.png")

labeled = 0
remove = 0
for idx, data in enumerate(png_files):
    data_name = data[:-4] + '.txt'

    if data_name in txt_files:
        labeled = labeled + 1
        
    else:
        os.system("rm " + data)
        remove = remove + 1


print('total img', len(png_files))
print('total label', len(txt_files))

print('labeled', labeled)
print('remove', remove)