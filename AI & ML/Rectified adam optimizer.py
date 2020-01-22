import keras
import numpy as np
from keras_radam import RAdam
from keras_radam.training import RAdamOptimizer
# Build toy model with RAdam optimizer
model = keras.models.Sequential()
model.add(keras.layers.Dense(input_shape=(17,), units=3))
model.compile(RAdam(), loss='mse')
# Generate toy data
x = np.random.standard_normal((4096 * 30, 17))
w = np.random.standard_normal((17, 3))
y = np.dot(x, w)
# Fit
model.fit(x, y, epochs=5)
RAdamOptimizer(learning_rate=1e-3)
RAdam(total_steps=10000, warmup_proportion=0.1, min_lr=1e-5)
