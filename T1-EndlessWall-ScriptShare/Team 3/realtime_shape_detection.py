# 13.11.22 // Shape Detection - Tr5 Nijat.M

import cv2
import numpy as np
from datetime import datetime
import json
from json import JSONEncoder


def nothing(x):
    # any operation
    pass


path = r'.\imgDB\Saved\14-080258_imgoutput.jpeg'
img = cv2.imread(path)

cap = img


# #Save the bricks contour with respect to the area
# date = datetime. now(). strftime("%d-%H%M%S")
# filename = f"{date}_imgoutput"
# cv2.imwrite(f'.\imgDB\Contours\{filename}.jpeg', imgoutput)
# print(filename + " _ " + "SAVED")


# Open a Json with execution date in Write mode
date = datetime. now(). strftime("%d-%H%M%S")
filename = f"{date}_imgoutput"
with open(f'.\imgDB\Contours\{filename}.json', 'w') as f:
    print("The json file is created")

tempContours = []

# np array to json encoder / Serializer


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


# Trackbar Creation
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 0, 180, nothing)
cv2.createTrackbar("L-S", "Trackbars", 28, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", 43, 180, nothing)
cv2.createTrackbar("U-S", "Trackbars", 59, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("AreaSlider", "Trackbars", 500, 5000, nothing)

font = cv2.FONT_HERSHEY_COMPLEX

while True:
    hsv = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")
    AreaSlider = cv2.getTrackbarPos("AreaSlider", "Trackbars")

    lower_red = np.array([l_h, l_s, l_v])
    upper_red = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)

    # Contours detection
    if int(cv2.__version__[0]) > 3:
        # Opencv 4.x.x
        contours, _ = cv2.findContours(
            mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:
        # Opencv 3.x.x
        _, contours, _ = cv2.findContours(
            mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # contour creation
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        # Drawing boxes according to its areas
        if area > 1200 and area < 5000:
            # draw a Contour around bricks
            cv2.drawContours(cap, [approx], 0, (0, 0, 0), 3)
            tempContours.append([approx])

            if len(approx) == 4:
                cv2.putText(cap, "Brick", (x, y), font, 1, (0, 0, 0))
    cv2.imshow("cap", cap)
    cv2.imshow("Mask", mask)

# Serializing the chaotic opencv IMG array
    numpyData = {"Contour Points": tempContours}
    encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)

# Writing to the json file
    print(tempContours)
    with open(f'.\imgDB\Contours\{filename}.json', "r+") as f:
        f.write(json.dumps(encodedNumpyData))

    # key = cv2.waitKey(1)
    cv2.waitKey(6000)  # delay in milliseconds
    cv2.destroyAllWindows()
    # if key == 27:
    #     break

cap.release()
cv2.destroyAllWindows()
