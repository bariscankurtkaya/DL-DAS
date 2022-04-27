import glob
import math
import numpy as np
import cv2 as cv


def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    channel_count = 2
    match_mask_color = (255,) * channel_count
    cv.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv.bitwise_and(img, mask)
    return masked_image


def calculate_distance(x0, y0, x_mid, y_bottom):
    distance = (x_mid - x0) * (x_mid - x0) + (y_bottom - y0) * (y_bottom - y0)
    return distance


def stretch_the_lines(l, height, width):
    # line = [x0, y0, x1, y1]
    x0 = l[0]
    y0 = l[1]
    x1 = l[2]
    y1 = l[3]

    if x0 != 0 and y0 != 0:
        slope = (y0 - y1) / (x1 - x0)
        bias = (height - y0) - (slope * x0)
        if bias > 0:
            x0 = 0
            y0 = height - bias
            if width * slope + bias < height:
                x1 = width
                y1 = height - (slope * width + bias)
            else:
                x1 = (height - bias) / slope
                y1 = 0
        else:
            x0 = -bias / slope
            y0 = height
            if width * slope + bias < height:
                x1 = width
                y1 = height - (slope * width + bias)
            else:
                x1 = (height - bias) / slope
                y1 = 0

    x0 = round(x0)
    y0 = round(y0)
    y1 = round(y1)
    x1 = round(x1)
    return [x0, y0, x1, y1]

# Added lines to image.
def create_lines(edges, height, width):
    probability_img = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)

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
            if abs(y0 - y1) > 20 and y0 != height and x0 != width / 2:
                distance = calculate_distance(x0, y0, width / 2, height)
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

    closest_left_point = stretch_the_lines(closest_left_point, height, width)
    closest_right_point = stretch_the_lines(closest_right_point, height, width)

    cv.line(probability_img, (closest_left_point[0], closest_left_point[1]),
            (closest_left_point[2], closest_left_point[3]), (0, 0, 255), 3,
            cv.LINE_AA)
    cv.line(probability_img, (closest_right_point[0], closest_right_point[1]),
            (closest_right_point[2], closest_right_point[3]), (0, 0, 255), 3,
            cv.LINE_AA)

    return probability_img


def create_long_lines(edges):
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


def show_all_images(*imgs):
    cv.imshow("Source", imgs[0])
    cv.imshow("Cropped Source", imgs[1])
    cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", imgs[2])
    cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", imgs[3])
    cv.waitKey()


if __name__ == "__main__":
    # 1418755682251300, 1418755735119099, 1425062189701993, 1425062278502329
    # Getting image properties and crop it
    img = (glob.glob("../Dataset/1425062278502329.png"))[0]
    img = cv.imread(img, cv.IMREAD_UNCHANGED)

    print(img.shape)
    height = img.shape[0] - 200
    width = img.shape[1]

    region_of_interest_vertices = [
        (0, height),
        (width / 2, height / 2),
        (width, height)
    ]

    roi = np.array([region_of_interest_vertices], np.int32)
    croppedImg = region_of_interest(img, roi)

    # Using canny edge detector and HoughLinesP to find road lines.
    edges = cv.Canny(croppedImg, 180, 220, None, 3)

    hough_img = create_long_lines(edges)
    hough_probability_img = create_lines(edges, height, width)

    show_all_images(img, croppedImg, hough_img, hough_probability_img)
