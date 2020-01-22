import cv2
import numpy as np
import matplotlib.pyplot as plt
fig = cv2.imread('D:/Pycharm/Program/AI_Stat_ANN/TajMahal.png', 0)
border = np.ones((5, 5), np.uint8)
erode = cv2.erode(fig, border, iterations=1)
dilated = cv2.dilate(fig, border, iterations=1)
plt.imshow(fig)
plt.show()
plt.imshow(erode)
plt.show()
plt.imshow(dilated)
plt.show()
cv2.waitKey(0)