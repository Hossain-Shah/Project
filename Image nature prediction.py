import numpy as np
from keras.layers import Conv2D, Activation, MaxPool2D, Flatten, Dense
from keras.models import Sequential
from keras.datasets import mnist
img_shape = (28,28,1)
model = Sequential()
model.add(Conv2D(6,2,input_shape=img_shape))
model.add(Activation('relu'))
model.add(MaxPool2D(2))
model.add(Flatten())
model.add(Dense(10))
model.add(Activation('softmax'))
model.summary()
model.compile(loss='sparse_categorical_crossentropy', optimizer = 'adam', metrics=['acc'])
(x_train, y_train), (x_test, y_test) = mnist.load_data()
print(x_train.shape)
x_train = np.expand_dims(x_train,-1)
x_test = np.expand_dims(x_test,-1)
print(x_train.shape)
print(y_train.shape)
model.fit(x_train,y_train,batch_size=32,epochs=10,validation_data=(x_test,y_test))

