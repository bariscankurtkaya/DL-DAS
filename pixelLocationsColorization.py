import glob
import cv2


def load_dataset(image_dir):
    return (glob.glob(image_dir + "/*.png"))


img_path_array = load_dataset("../")

for l in range(len(img_path_array)):
    img = cv2.imread(img_path_array[l] , 0)
    img = img[0:200]
    
        
cv2.imshow(img_path_array[-1],img)
cv2.waitKey(0)
cv2.destroyAllWindows()
