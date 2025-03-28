import cv2 as cv
from matplotlib import pyplot as plt
image = cv.imread('TajMahal.jpg',0)
edges = cv.Canny(image,100,200)
plt.subplot(121),plt.imshow(image,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Canny Effected Edged Image'), plt.xticks([]), plt.yticks([])
plt.show()