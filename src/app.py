from lineDetection import LaneDetection
from dnClassifier import DNClassifier

import glob
import cv2 as cv


# classes = [carBumper = 0, person = 1]


class App:
    def __init__(self):
        self.img = (glob.glob("../Dataset/1425062278502329.png"))[0]
        self.img = cv.imread(self.img, cv.IMREAD_UNCHANGED)
        self.is_ony_line_preview = True
        self.dn_classifier = DNClassifier()
        self.lane_detection = LaneDetection()

        # predicted_coordinates = [class, probability, x0, y0, width, height]
        self.predicted_coordinates = []

    def test_dn_lassifier(self):
        return self.dn_classifier.thresholdTestForOneImage(self.img)

    def predict_coordinates(self, is_night):
        if is_night:
            # selects the our model
            print("Our Model")
            self.predicted_coordinates = [[0, 89, 250, 250, 500, 500], [1, 92, 100, 100, 400, 400]]
        else:
            # selects the YoloV4 coco model
            print("YoloV4 COCO")
            self.predicted_coordinates = [[0, 60, 250, 250, 500, 500], [1, 88, 250, 250, 600, 600]]

    def img_lane_detection(self):
        self.lane_detection.main(self.img, self.predicted_coordinates, self.is_ony_line_preview, )


if __name__ == "__main__":
    print("Welcome to Driver Assistance System! Your life is important.")
    app = App()

    # image will read

    # Then dnClassifier thresholdTestForOneImage function will called
    is_night = app.test_dn_lassifier()

    # Deep Learning model selection and class coordinate return
    app.predict_coordinates(is_night)

    # Calls lineDetection function
    app.img_lane_detection()
