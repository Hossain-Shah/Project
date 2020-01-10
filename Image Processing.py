from scipy import misc
ascent = misc.ascent()
import matplotlib.pyplot as plt
image = plt.imread('IMG_20170323_104738.jpg')
plt.gray()
plt.axis("off")
print(image)
plt.imshow(image)
plt.show()