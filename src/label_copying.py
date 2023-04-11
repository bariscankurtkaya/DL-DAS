import os
from glob import glob

dataset_dir = "/data/scratch/bariskurtkaya/oxford/yolo/2014-11-14-16-34-33/stereo/centre/"

txt_files = glob(dataset_dir+ "*.txt")

for idx, data in enumerate(txt_files):

    data_dir = data[:-4]

    for i in range(20):

        command = f"cp {data} {data_dir}_{i+1}.txt"

        os.system(command)
    
    print(idx)