import cv2
img = cv2.imread("F:/Photos/Campus life(Tangail)/WP_20151012_14_40_59_Pro.jpg")
result = cv2.fastNlMeansDenoisingColored(img,None,20,10,7,21)
cv2.imshow("Original Image", img)

cv2.imshow("Denoised Image", result)

cv2.waitKey(0)