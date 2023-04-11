import torch
import torch.nn as nn

from torchvision import transforms

import kornia.augmentation as K

import cv2 as cv
import numpy as np

from tqdm import tqdm

from glob import glob

torch.manual_seed(0)

transform_to_tensor = transforms.ToTensor()

aug_transform = nn.Sequential(
    #K.RandomPlanckianJitter("blackbody", same_on_batch=False, keepdim=False, p=1.0),
    #K.RandomPlasmaShadow(roughness=(0.1, 0.7), shade_intensity=(-1.0, 0.0), shade_quantity=(0.0, 1.0), same_on_batch=False, keepdim=False, p=1.0),
    #K.RandomPlasmaBrightness(roughness=(0.1, 0.7), intensity=(0.0, 1.0), same_on_batch=False, keepdim=False, p=1.0),
    #K.RandomPlasmaContrast(roughness=(0.1, 0.7), same_on_batch=False, keepdim=False, p=1.0),
    K.ColorJiggle(0.3, 0.3, 0.3, 0.3, same_on_batch=False, keepdim=False, p=1.0),
    K.ColorJitter(0.3, 0.3, 0.3, 0.3, same_on_batch=False, keepdim=False, p=1.0),
    #K.RandomBoxBlur((21, 5), "reflect", same_on_batch=False, keepdim=False, p=1.0),
    K.RandomBrightness(brightness=(0.8, 1.2), clip_output=True, same_on_batch=False, keepdim=False, p=1.0),
    #K.RandomChannelShuffle(same_on_batch=False, keepdim=False, p=1.0),
    K.RandomContrast(contrast=(0.8, 1.2), clip_output=True, same_on_batch=False, keepdim=False, p=1.0),
    #K.RandomEqualize(same_on_batch=False, keepdim=False, p=1.0),
    K.RandomGamma((0.2, 1.3), (1.0, 1.5), same_on_batch=False, keepdim=False, p=1.0),
    #K.RandomGrayscale(same_on_batch=False, keepdim=False, p=1.0),
    #K.RandomGaussianBlur((21, 21), (0.2, 1.3), "reflect", same_on_batch=False, keepdim=False, p=1.0),
    K.RandomSharpness((0.5, 1.0), same_on_batch=False, keepdim=False, p=1.0),
    #K.RandomGaussianNoise(mean=0.01, std=0.05, same_on_batch=False, keepdim=False, p=1.0),
    K.RandomHue((-0.2, 0.4), same_on_batch=False, keepdim=False, p=1.0),
    #K.RandomMotionBlur((7, 7), 35.0, 0.5, "reflect", "nearest", same_on_batch=False, keepdim=False, p=1.0)
)

dataset_dir = '/data/scratch/bariskurtkaya/oxford/yolo/2014-11-14-16-34-33/stereo/centre/*.png'

for _, data_dir in tqdm(enumerate(glob(dataset_dir))):
    img = cv.imread(data_dir)
    
    tensor = transform_to_tensor(img)
            
    for idx in range(20):
        aug_img = tensor.numpy().transpose(1, 2, 0)

        new_data_dir = data_dir[:-4] + f"_{idx+1}.png"

        cv.imwrite(new_data_dir, aug_img)