import glob
import math
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    channel_count = 2
    match_mask_color = (255,) * channel_count
    cv.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv.bitwise_and(img, mask)
    return masked_image


if __name__ == "__main__":
    # 1418755682251300
    # 1418755735119099
    # 1425062189701993
    # 1425062278502329
    img = (glob.glob("../Dataset/1425062189701993.png"))[0]

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

    edges = cv.Canny(croppedImg, 200, 240, None, 3)

    cdstP = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)

    """
    lines = cv.HoughLines(edges, 1, np.pi / 180, 100, None, 0, 0)

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            cv.line(cdst, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)

    """
    linesP = cv.HoughLinesP(edges, 1, np.pi / 180, 50, None, 50, 10)

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            if abs(l[1] - l[3]) > 20:
                # img, (x,y), (x,y), color, thickness,linetype
                cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv.LINE_AA)

    cv.imshow("Source", img)
    cv.imshow("Cropped Source", croppedImg)
    # cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)

    cv.waitKey()
