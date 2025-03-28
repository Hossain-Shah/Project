import numpy as np
import cv2
import matplotlib.pyplot as plt
test_image = cv2.imread('D:/Pycharm/Program/AI,Stat & ANN/20180404_120426.jpg')
test_image_gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
plt.imshow(test_image_gray, cmap='gray')


def convertToRGB(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


haar_cascade_face = cv2.CascadeClassifier('D:/Anaconda/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
faces_rects = haar_cascade_face.detectMultiScale(test_image_gray, scaleFactor = 1.2, minNeighbors = 5)
print('Faces found: ', len(faces_rects))
plt.imshow(convertToRGB(test_image))


