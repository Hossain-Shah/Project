import cv2
import numpy as np
import matplotlib.pyplot as plt
img = cv2.imread('fire-flames-on-black-background-260nw-736335832.jpg')
lower_bound = np.array([11, 33, 111])
upper_bound = np.array([90, 255, 255])
img = cv2.resize(img, (1280, 720))
img = cv2.flip(img, 1)
frame_smooth = cv2.GaussianBlur(img, (7, 7), 0)
mask = np.zeros_like(img)
mask[0:720, 0:1280] = [255, 255, 255]
img_roi = cv2.bitwise_and(frame_smooth, mask)
frame_hsv = cv2.cvtColor(img_roi, cv2.COLOR_BGR2HSV)
image_binary = cv2.inRange(frame_hsv, lower_bound, upper_bound)
check_if_fire_detected = cv2.countNonZero(image_binary)
if int(check_if_fire_detected) >= 20000:
    cv2.putText(img, "Fire Detected !", (300, 60), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 2)
cv2.imshow("Fire Detection", img)
cv2.waitKey(0)

