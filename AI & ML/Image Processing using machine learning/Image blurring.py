import cv2
import numpy as np
from matplotlib import pyplot as plt
fig = cv2.imread('D:/Pycharm/Program/AI,Stat & ANN/TajMahal.png')
blurred = cv2.blur(fig,(5,5))
plt.subplot(121),plt.imshow(fig),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(blurred),plt.title('Blurred')
plt.xticks([]), plt.yticks([])
plt.show()