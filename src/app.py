import lineDetection
from dnClassifier import DNClassifier

import glob
import cv2 as cv


class App:
    def __init__(self):
        self.img = (glob.glob("../Dataset/1425062278502329.png"))[0]
        self.img = cv.imread(self.img, cv.IMREAD_UNCHANGED)
        self.dn_classifier = DNClassifier()

    def testDNClassifier(self):
        return self.dn_classifier.thresholdTestForOneImage(self.img)

    def selectTheDeepLearningModel(self, isNight):
        coordinates = [250, 250, 500, 500]
        if isNight:
            # selects the our model
            print("Our Model")
        else:
            # selects the YoloV4 coco model
            print("YoloV4 COCO")

        return coordinates


if __name__ == "__main__":
    print("Welcome to Driver Assistance System! Your life is important.")
    app = App()

    # image will read

    # Then dnClassifier thresholdTestForOneImage function will called
    isNight = app.testDNClassifier()

    # Deep Learning model selection and class coordinate return
    coordinates = app.selectTheDeepLearningModel()


