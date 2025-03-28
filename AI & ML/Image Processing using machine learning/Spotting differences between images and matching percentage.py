# import module
from PIL import Image, ImageChops
import numpy, cv2
# assign images
img1 = Image.open("F:/Photos/Me/IMG_0898.JPG")
img2 = Image.open("F:/Photos/Me/IMG_0899.JPG")
# finding difference
diff = ImageChops.difference(img1, img2)
# showing the difference
diff.show()
img1 = cv2.imread('F:/Photos/Me/IMG_0898.JPG', 0)
img2 = cv2.imread('F:/Photos/Me/IMG_0899.JPG', 0)
#--- take the absolute difference of the images ---
res = cv2.absdiff(img1, img2)
#--- convert the result to integer type ---
res = res.astype(numpy.uint8)
#--- find percentage difference based on number of pixels that are not zero ---
percentage = (numpy.count_nonzero(res) * 100)/res.size
print(percentage)
