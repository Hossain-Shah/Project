import cv2 as cv
import matplotlib.pyplot as plt
depth = cv.CV_16S
size = 3
image = plt.imread('TajMahal.jpg')
plt.imshow(image)
plt.show()
plt.gray()
plt.axis("off")
laplacian_operator = cv.Laplacian(image, depth, ksize=size)
laplacian_impact_on_image = cv.convertScaleAbs(laplacian_operator)
plt.imshow(laplacian_impact_on_image)
plt.show()



