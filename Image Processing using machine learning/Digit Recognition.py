from sklearn.datasets import *
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import numpy as np


def Image_display(i):
   plt.imshow(digit['images'][i],cmap = 'Greys_r')
   plt.show()


digit = load_digits()
digit_d = pd.DataFrame(digit['data'][0:1600])

train_x = digit['data'][:1600]
train_y = digit['target'][:1600]
KNN = KNeighborsClassifier(20)
KNN.fit(train_x,train_y)
KNeighborsClassifier(algorithm = 'auto', leaf_size = 30, metric = 'minkowski',metric_params = None, n_jobs = 1, n_neighbors = 20, p = 2,weights = 'uniform')
test = np.array(digit['data'][1725])
test1 = test.reshape(1,-1)
Image_display(1725)
print(KNN.predict(test1))
print(digit['target_names'])