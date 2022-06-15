from lineDetection import LaneDetection
from dnClassifier import DNClassifier

import glob
import cv2 as cv


# classes = [carBumper = 0, person = 1]


class App:
    def __init__(self):
        self.is_ony_line_preview = True
        self.dn_classifier = DNClassifier()
        self.lane_detection = LaneDetection()

        # cnn_predicted_coordinates = [[class, probability, x0, y0, width, height]]
        self.cnn_predicted_coordinates = []

    def test_dn_lassifier(self, img):
        return self.dn_classifier.thresholdTestForOneImage(img)

    def cnn_predicted_coordinates(self, is_night):
        if is_night:
            # selects the our model
            print("Our Model")
            self.cnn_predicted_coordinates = [[0, 89, 250, 250, 500, 500], [1, 92, 100, 100, 400, 400]]
        else:
            # selects the YoloV4 coco model
            print("YoloV4 COCO")
            self.cnn_predicted_coordinates = [[0, 60, 250, 250, 500, 500], [1, 88, 250, 250, 600, 600]]

    def img_lane_detection(self, img):
        cnn_predicted_coordinates = [[0, 88, 550, 550, 199, 200]]

        self.lane_detection.main(img, cnn_predicted_coordinates, self.is_ony_line_preview)


if __name__ == "__main__":
    print("Welcome to Driver Assistance System! Your life is important.")
    app = App()

    img_list = (glob.glob("/Volumes/Barışcan HDD/tubitak-2209/Dataset/Gece/1/stereo/centre/*"))

    for i in range(len(img_list) - 3000):
        img = cv.imread(img_list[i+3000], cv.IMREAD_UNCHANGED)
        # Then dnClassifier thresholdTestForOneImage function will called
        is_night = app.test_dn_lassifier(img)
        print(is_night)
        # Deep Learning model selection and class coordinate return
        #app.cnn_predicted_coordinates(is_night)

        # Calls lineDetection function
        app.img_lane_detection(img)
