import glob
import math
import numpy as np
import cv2 as cv

rad_to_degree = 57.2958

left_arrow = cv.imread((glob.glob("../Dataset/left_arrow.jpeg"))[0], cv.IMREAD_UNCHANGED)
right_arrow = cv.imread((glob.glob("../Dataset/right_arrow.png"))[0], cv.IMREAD_UNCHANGED)
stop_sign = cv.imread((glob.glob("../Dataset/stop_sign.jpg"))[0], cv.IMREAD_UNCHANGED)
check_sign = cv.imread((glob.glob("../Dataset/check_sign.jpeg"))[0], cv.IMREAD_UNCHANGED)

left_arrow = cv.cvtColor(left_arrow, cv.COLOR_BGR2GRAY)
right_arrow = cv.cvtColor(right_arrow, cv.COLOR_BGR2GRAY)
stop_sign = cv.cvtColor(stop_sign, cv.COLOR_BGR2GRAY)
check_sign = cv.cvtColor(check_sign, cv.COLOR_BGR2GRAY)

res_left_arrow = cv.resize(left_arrow, dsize=(1280, 960), interpolation=cv.INTER_CUBIC)
res_right_arrow = cv.resize(right_arrow, dsize=(1280, 960), interpolation=cv.INTER_CUBIC)
res_stop_sign = cv.resize(stop_sign, dsize=(1280, 960), interpolation=cv.INTER_CUBIC)
res_check_sign = cv.resize(check_sign, dsize=(1280, 960), interpolation=cv.INTER_CUBIC)

print(left_arrow.shape)
print(res_left_arrow.shape)


class Point(object):
    def __init__(self):
        self.coordinates = [0, 0, 0, 0]
        self.slope = 0
        self. bias = 0


class LaneDetection:
    def __init__(self):
        self.cnn_predicted_coordinates = []
        self.total_predicted_class_count = 0

        self.height = 0
        self.width = 0
        self.img = img

        self.left_point = Point()
        self.right_point = Point()

    def check_and_import_image(self):
        car_headlight_height = self.height - 195
        if self.left_point.coordinates[1] < car_headlight_height < self.right_point.coordinates[3]:
            self.img = np.concatenate((self.img, res_left_arrow), axis=1)
        elif self.left_point.coordinates[1] > car_headlight_height > self.right_point.coordinates[3]:
            self.img = np.concatenate((self.img, res_right_arrow), axis=1)
        else:
            self.img = np.concatenate((self.img, res_check_sign), axis=1)

    def region_of_interest(self, vertices):
        mask = np.zeros_like(self.img)
        channel_count = 2
        match_mask_color = (255,) * channel_count
        cv.fillPoly(mask, vertices, match_mask_color)
        masked_image = cv.bitwise_and(self.img, mask)
        return masked_image

    def calculate_distance(self, x0, y0, x_mid, y_bottom):
        distance = (x_mid - x0) * (x_mid - x0) + (y_bottom - y0) * (y_bottom - y0)
        return distance

    def stretch_the_lines(self, closestPoint):
        # line = [x0, y0, x1, y1]
        x0 = closestPoint[0]
        y0 = closestPoint[1]
        x1 = closestPoint[2]
        y1 = closestPoint[3]

        if x1 == x0:
            x0 = abs(x1 - 1)

        if x0 != 0 and y0 != 0:
            slope = (y0 - y1) / (x1 - x0)
            print("slope:", slope)
            bias = (self.height - y0) - (slope * x0)
            if x0 < 640:
                self.left_point.slope = slope
                self.left_point.bias = bias
            else:
                self.right_point.slope = slope
                self.right_point.bias = bias

            if bias > 0:
                x0 = 0
                y0 = self.height - bias
                if self.width * slope + bias < self.height:
                    x1 = self.width
                    y1 = self.height - (slope * self.width + bias)
                else:
                    x1 = (self.height - bias) / slope
                    y1 = 0
            else:
                x0 = -bias / slope
                y0 = self.height
                if self.width * slope + bias < self.height:
                    x1 = self.width
                    y1 = self.height - (slope * self.width + bias)
                else:
                    x1 = (self.height - bias) / slope
                    y1 = 0

        print(closestPoint, x0, x1, y0, y1)
        x0 = round(x0)
        y0 = round(y0)
        y1 = round(y1)
        x1 = round(x1)
        return [x0, y0, x1, y1]

    # Added lines to image.
    def create_lines(self, edges):
        height = self.height
        width = self.width

        # probability_img = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)

        linesP = cv.HoughLinesP(edges, 1, np.pi / 180, 50, None, 50, 10)

        if linesP is not None:
            closest_left_point = [0, 0, 0, 0]
            closest_left_distance = width * width + height * height

            closest_right_point = [0, 0, 0, 0]
            closest_right_distance = width * width + height * height

            for i in range(0, len(linesP)):
                l = linesP[i][0]
                x0 = l[0]
                y0 = l[1]
                x1 = l[2]
                y1 = l[3]
                # arctan(y/x) > 20 || 30 derece üstü kontrolü yapılacak
                # print(math.atan(y/x)* 57.2958) > 20 || 30
                if abs(math.atan((y1 - y0) / (x1 - x0)) * rad_to_degree) > 10 and y0 != height and x0 != width / 2:
                    distance = self.calculate_distance(x0, y0, width / 2, height)
                    if x0 < width / 2:
                        if closest_left_distance > distance:
                            closest_left_point = [x0, y0, x1, y1]
                            closest_left_distance = distance
                            print("left min: ", distance, closest_left_point)
                        else:
                            continue
                    else:
                        if closest_right_distance > distance:
                            closest_right_point = [x0, y0, x1, y1]
                            closest_right_distance = distance
                            print("right min: ", distance, closest_right_point)
                        else:
                            continue

        self.left_point.coordinates = self.stretch_the_lines(closest_left_point)
        self.right_point.coordinates = self.stretch_the_lines(closest_right_point)

        self.draw_lines()
        # self.draw_lines(probability_img, closest_left_point, closest_right_point)

    def draw_lines(self):
        cv.line(self.img, (self.left_point.coordinates[0], self.left_point.coordinates[1]),
                (self.left_point.coordinates[2], self.left_point.coordinates[3]), (0, 0, 255), 3,
                cv.LINE_AA)
        cv.line(self.img, (self.right_point.coordinates[0], self.right_point.coordinates[1]),
                (self.right_point.coordinates[2], self.right_point.coordinates[3]), (0, 0, 255), 3,
                cv.LINE_AA)

    def create_long_lines(self, edges):
        cdst = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)

        lines = cv.HoughLines(edges, 1, np.pi / 180, 100, None, 0, 0)

        if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                if theta < 1.2:
                    a = math.cos(theta)
                    b = math.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
                    pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
                    cv.line(cdst, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)
        return cdst

    def show_all_images(self, *imgs):
        # cv.imshow("Source", imgs[0])
        cv.imshow("Cropped Source", imgs[0])
        # cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", imgs[2])
        cv.imshow("Result", imgs[1])
        cv.waitKey()

    def main(self, img, cnn_predicted_coordinates, isPreview):
        self.cnn_predicted_coordinates = cnn_predicted_coordinates
        self.total_predicted_class_count = len(self.cnn_predicted_coordinates)

        self.img = img
        print(self.img.shape)
        self.height = img.shape[0]
        self.width = img.shape[1]

        region_of_interest_vertices = [
            (0, self.height - 200),
            (self.width / 2, (self.height - 200) / 2),
            (self.width, (self.height - 200))
        ]

        roi = np.array([region_of_interest_vertices], np.int32)
        croppedImg = self.region_of_interest(roi)

        # Using canny edge detector and HoughLinesP to find road lines.
        edges = cv.Canny(croppedImg, 180, 220, None, 3)

        # hough_img = create_long_lines(edges)
        self.create_lines(edges)
        self.check_and_import_image()

        if isPreview:
            # print(hough_probability_img.shape)
            self.show_all_images(croppedImg, self.img)


if __name__ == "__main__":
    # 1418755682251300, 1418755735119099, 1425062189701993, 1425062278502329
    # Risky ones -> 1418236403008951, 1418236511931591, 1418236571236006, 1425062029911396, 1425062191889195, 1425062338806569
    # "../Dataset/1418755682251300.png"
    # Getting image properties and crop it
    # "/media/bkurtkaya/Barışcan HDD/darknet/build/darknet/x64/test/geceDeneme/YoloTest/1418755829356268.png"
    img = (glob.glob("../Dataset/1418755682251300.png"))[0]
    # img = (glob.glob("/Volumes/Barışcan HDD/tubitak-2209/Dataset/1418236403008951.png"))[0]
    img = cv.imread(img, cv.IMREAD_UNCHANGED)
    isPreview = True

    # cnn_predicted_coordinates = [[class, prob, x0, y0, width, height]]
    cnn_predicted_coordinates = [[0, 90, 475, 425, 100, 75]]
    laneDetection = LaneDetection()
    laneDetection.main(img, cnn_predicted_coordinates, isPreview)
