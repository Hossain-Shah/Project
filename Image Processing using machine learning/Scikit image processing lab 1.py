import os
from skimage import data,io,filters
camera = data.camera()
type(camera)
print(camera.shape)
coins = data.coins()
threshold_value = filters.threshold_otsu(coins)
print(threshold_value)
file = os.path.join('TajMahal.jpg')
cars = io.imread(file)
io.imshow(cars)
io.show()