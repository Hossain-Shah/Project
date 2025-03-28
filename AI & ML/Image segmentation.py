from skimage import data
import numpy as np
import skimage.data as data
import skimage.segmentation as seg
import skimage.filters as filters
import skimage.draw as draw
import skimage.color as color
import matplotlib.pyplot as plt
image = data.astronaut()
plt.imshow(image)
plt.show()


def image_show(image, nrows=1, ncols=1, cmap='gray'):
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(14, 14))
    ax.imshow(image, cmap='gray')
    ax.axis('off')
    return fig, ax


image_gray = color.rgb2gray(image)
image_show(image)


def circle_points(resolution, center, radius):
    radians = np.linspace(0, 2 * np.pi, resolution)
    c = center[1] + radius * np.cos(radians)
    r = center[0] + radius * np.sin(radians)

    return np.array([c, r]).T


points = circle_points(200, [80, 250], 80)[:-1]
snake = seg.active_contour(image_gray, points,alpha=0.06,beta=0.3)
fig, ax = image_show(image_gray)
ax.plot(points[:, 0], points[:, 1], '--r', lw=3)
ax.plot(snake[:, 0], snake[:, 1], '-b', lw=3)
plt.show()
image_labels = np.zeros(image_gray.shape, dtype=np.uint8)
indices = draw.circle_perimeter(80, 250,20)
image_labels[indices] = 1
image_labels[points[:, 1].astype(np.int), points[:, 0].astype(np.int)] = 2
image_show(image_labels)
plt.show()
image_felzenszwalb = seg.felzenszwalb(image)
image_show(image_felzenszwalb)
plt.show()
image_felzenszwalb_colored = color.label2rgb(image_felzenszwalb, image, kind='avg')
image_show(image_felzenszwalb_colored)
plt.show()
