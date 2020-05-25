from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import matplotlib.pyplot as plt
import os
from keras.preprocessing import image
import numpy as np
from PIL import Image
print(os.listdir("D:/Pycharm/Program/AI_Stat_ANN/Dataset1"))
img_width, img_height = 128, 128
nb_train_samples = 7
nb_validation_samples = 7
epochs = 2
batch_size = 2
if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)
model = Sequential()
model.add(Conv2D(32, (2, 2), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(32, (2, 2)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (2, 2)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(3))
model.add(Activation('softmax'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1. / 255)
train = train_datagen.flow_from_directory('D:/Pycharm/Program/AI_Stat_ANN/Dataset1/train',
                                                    target_size=(img_width, img_height),
                                                    batch_size=batch_size, class_mode='categorical')
test = test_datagen.flow_from_directory(
    'D:/Pycharm/Program/AI_Stat_ANN/Dataset1/test',
    target_size=(img_width, img_height),
    batch_size=batch_size, class_mode='categorical')
model.fit_generator(train,
                    steps_per_epoch=nb_train_samples // batch_size,
                    epochs=epochs, validation_data=test,
                    validation_steps=nb_validation_samples // batch_size)
test_image = image.load_img('F:/Photos/Friends & Family(Dhaka)/66045093_574584506403468_3965628860145336320_n.jpg', target_size=(img_width, img_height))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis=0)
result = model.predict(test_image)
classes = np.array(['asset', 'empowered', 'liability'])
top_3 = np.argsort(result[0])[:-4:-1]
for i in range(3):
    print("{}".format(classes[top_3[i]])+" ({:.3})".format(result[0][top_3[i]]))
print(result)
itemindex = np.where(result == np.max(result))
print("probability:" + str(np.max(result)) + "\n" + classes[itemindex[1][0]])
