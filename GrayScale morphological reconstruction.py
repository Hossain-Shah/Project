import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import reconstruction
x = np.linspace(0, 4 * np.pi)
y_mask = np.cos(x)
y_seed = y_mask.min() * np.ones_like(x)
y_seed[-1] = 0
y_reconstruction = reconstruction(y_seed, y_mask)
y, x = np.mgrid[:20:0.5, :20:0.5]
bumps = np.sin(x) + np.sin(y)
filter = 0.3
seed = bumps - filter
background = reconstruction(seed, bumps)
perfection = bumps - background
plt.imshow(perfection, cmap=plt.get_cmap('gray'))
plt.show()
