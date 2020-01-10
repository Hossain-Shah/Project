from skimage import data
import matplotlib.pyplot as plt
image = data.camera()
type(image)
mask = image < 87
image[mask] = 255
plt.imshow(image, cmap='gray')
plt.show()