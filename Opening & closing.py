import cv2
import numpy as np
import matplotlib.pyplot as plt
fig = cv2.imread('D:/Pycharm/Program/AI,Stat & ANN/TajMahal.png', 0)
border = np.ones((5, 5), np.uint8)
open = cv2.morphologyEx(fig,cv2.MORPH_OPEN, border, iterations=1)
close = cv2.morphologyEx(fig, cv2.MORPH_CLOSE,border, iterations=1)
plt.imshow(fig)
plt.show()
plt.imshow(open)
plt.show()
plt.imshow(close)
plt.show()
cv2.waitKey(0)