from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt
im = Image.open("D:/Pycharm/Program/AI,Stat & ANN/TajMahal.jpg")
im.rotate(45).show()
print(im)
print(im.size)
print(im.format)
im.save('TajMahal.png')
im.thumbnail((300, 300))
im.show()
TajMahal_gray = Image.open('TajMahal.jpg').convert('L')
TajMahal_gray.show()
im = cv2.imread('TajMahal.jpg',cv2.IMREAD_GRAYSCALE)
cv2.imshow('image',im)
cv2.waitKey(0)
cv2.destroyAllWindows()
im = cv2.imread('TajMahal.jpg',cv2.IMREAD_GRAYSCALE)
plt.imshow(im, cmap = 'gray', interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])
plt.plot([200,300,400],[100,200,300],'c', linewidth = 5)
plt.show()