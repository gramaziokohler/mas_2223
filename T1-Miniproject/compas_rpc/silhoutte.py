import cv2
import numpy as np
import sys
from compas.geometry import Polyline, Point, Curve

def get_contours(path = None, t_val = 100):
    img = cv2.imread(path)
    scale_percent = 60 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)

    dim = width, height
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


    img_blur = cv2.bilateralFilter(img, d = 7, sigmaSpace = 75, sigmaColor =75)
    # Convert to grayscale
    img_gray = cv2.cvtColor(img_blur, cv2.COLOR_RGB2GRAY)
    # Apply the thresholding
    a = img_gray.max()
    _, thresh = cv2.threshold(img_gray, a/2 + t_val, a,cv2.THRESH_BINARY_INV)
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find the contour of the figure
    contours, hierarchy = cv2.findContours(image = thresh,mode = cv2.RETR_TREE, method = cv2.CHAIN_APPROX_SIMPLE)

    # Sort the contours
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    # Draw the contour
    img_copy = img.copy()
    final = cv2.drawContours(img_copy, contours, contourIdx = -1, color = (255, 0, 0), thickness = 2)

    #create a compas polyline to view/use
    points = [[Point(p[0][0], p[0][1], 0) for p in plist] for plist in contours]
    polyline = [Polyline(points=p) for p in points]

    return polyline, img.shape
