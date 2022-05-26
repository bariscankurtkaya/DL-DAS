import glob
import math
import numpy as np
import cv2 as cv
from PIL import Image

left_arrow = cv.imread((glob.glob("../Dataset/left_arrow.jpeg"))[0], cv.IMREAD_UNCHANGED)
right_arrow = cv.imread((glob.glob("../Dataset/right_arrow.png"))[0], cv.IMREAD_UNCHANGED)
stop_sign = cv.imread((glob.glob("../Dataset/stop_sign.jpg"))[0], cv.IMREAD_UNCHANGED)
check_sign = cv.imread((glob.glob("../Dataset/check_sign.jpg"))[0], cv.IMREAD_UNCHANGED)

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


def check_and_import_image(img, closest_left_point, closest_right_point, height):
    car_headlight_height = height
    if closest_left_point[1] < car_headlight_height < closest_right_point[3]:
        img = np.concatenate((img, res_left_arrow), axis=1)
    elif closest_left_point[1] > car_headlight_height > closest_right_point[3]:
        img = np.concatenate((img, res_right_arrow), axis=1)
    else:
        img = np.concatenate((img, res_check_sign), axis=1)

    return img


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

    if x1 == x0:
        x0 = abs(x1 - 1)

    if x0 != 0 and y0 != 0 and y0 > 550:
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

    print(l, x0, x1, y0, y1)
    x0 = round(x0)
    y0 = round(y0)
    y1 = round(y1)
    x1 = round(x1)
    return [x0, y0, x1, y1]


# Added lines to image.
def create_lines(edges, height, width, img):
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

    draw_lines(img, closest_left_point, closest_right_point)
    draw_lines(probability_img, closest_left_point, closest_right_point)

    new_img = check_and_import_image(img, closest_left_point, closest_right_point, height)
    return [probability_img, new_img]


def draw_lines(img, closest_left_point, closest_right_point):
    cv.line(img, (closest_left_point[0], closest_left_point[1]),
            (closest_left_point[2], closest_left_point[3]), (0, 0, 255), 3,
            cv.LINE_AA)
    cv.line(img, (closest_right_point[0], closest_right_point[1]),
            (closest_right_point[2], closest_right_point[3]), (0, 0, 255), 3,
            cv.LINE_AA)
    return img


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
    cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", imgs[2])
    cv.imshow("Result", imgs[3])
    cv.waitKey()


if __name__ == "__main__":
    # 1418755682251300, 1418755735119099, 1425062189701993, 1425062278502329
    # Risky ones -> 1418236403008951, 1418236511931591, 1418236571236006, 1425062029911396, 1425062191889195, 1425062338806569
    # "../Dataset/1418755682251300.png"
    # Getting image properties and crop it
    # "/media/bkurtkaya/Barışcan HDD/darknet/build/darknet/x64/test/geceDeneme/YoloTest/1418755829356268.png"
    img = (glob.glob("../Dataset/gece1.1/1418755700623798.png"))[0]
    img = cv.imread(img, cv.IMREAD_UNCHANGED)

    print(img.shape)
    height = img.shape[0]
    width = img.shape[1]

    region_of_interest_vertices = [
        (0, height - 200),
        (width / 2, (height - 200) / 2),
        (width, (height - 200))
    ]

    roi = np.array([region_of_interest_vertices], np.int32)
    croppedImg = region_of_interest(img, roi)

    # Using canny edge detector and HoughLinesP to find road lines.
    edges = cv.Canny(croppedImg, 180, 220, None, 3)

    # hough_img = create_long_lines(edges)
    [hough_probability_img, new_img] = create_lines(edges, height, width, img)

    print(hough_probability_img.shape)
    show_all_images(img, croppedImg, hough_probability_img, new_img)
