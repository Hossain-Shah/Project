import cv2
import numpy as np
from matplotlib import pyplot as plt
fig = cv2.imread('D:/Pycharm/Program/AI,Stat & ANN/TajMahal.png')
border = np.ones((5,5),np.float32)/25
avg = cv2.filter2D(fig,-1,border)
plt.subplot(121),plt.imshow(fig),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(avg),plt.title('Averaging')
plt.xticks([]), plt.yticks([])
plt.show()
