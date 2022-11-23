# 12.11.22 // Perspective Wrap - Tr2 Nijat.M

import math
import numpy as np
import cv2
from datetime import datetime

path = r'.\imgDB\Timer\2022_11_14_07_46_21_766.jpg'
img = cv2.imread(path)


# Base corners for Tr2 --- 287, 89 / 1509, 99 / 1505, 1103 / 272, 1095

# arbitrary dimensions which should be related with real base dim...
width, height = 1120, 920


# Points on input image
pts1 = np.float32([[287, 91], [1509, 101], [1505, 1103], [272, 1095]])
# Aimed points for translation
pts2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
# Transformation Matrix for Warp
matrix = cv2.getPerspectiveTransform(pts1, pts2)
# Execution of Perspective Warp
imgoutput = cv2.warpPerspective(img, matrix, (width, height))

# Corner/Points Visualisation
for x in range(4):

    cv2.circle(img, (int(pts1[x][0]), int(pts1[x][1])),
               5, (0, 0, 255), cv2.FILLED)


# Save Image
date = datetime. now(). strftime("%d-%H%M%S")
filename = f"{date}_imgoutput"
cv2.imwrite(f'.\imgDB\Saved\{filename}.jpeg', imgoutput)
print(filename + " _ " + "SAVED")

# Visualisation of Initial and Final image
cv2.imshow("img", img)
cv2.imshow("Output Image", imgoutput)
cv2.waitKey(2000)  # delay in milliseconds
cv2.destroyAllWindows()
