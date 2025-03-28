import matplotlib.pyplot as plt
from skimage import data, filters
image = data.coins()
edges = filters.sobel(image)
plt.imshow(edges, cmap='gray')
plt.show()
