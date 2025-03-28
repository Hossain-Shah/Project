import cv2
f = cv2.imread('IMG_20170323_104738.jpg')
cv2.imshow('Original', f)
cv2.waitKey()
cv2.imshow('Grayscale', f)
cv2.waitKey()
