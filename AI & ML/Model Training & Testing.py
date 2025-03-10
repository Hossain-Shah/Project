from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import matplotlib.pyplot as plt
import os, pickle
from os import listdir
from keras.preprocessing import image
import numpy as np
from PIL import Image
import cv2
from sklearn.preprocessing import LabelBinarizer
from keras.optimizers import Adam
from keras.layers.normalization import BatchNormalization
from keras.preprocessing.image import img_to_array
from keras.models import load_model
img_width, img_height = 224, 224
epochs = 30
INIT_LR = 1e-3
batch_size = 32
image_size = 0
default_image_size = tuple((224, 224))
depth = 3
nb_train_samples = 11207
nb_validation_samples = 4804
directory_root = 'D:/Official purpose/Sprint - 27/Custom_dataset_for_tomato'


def convert_image_to_array(image_dir):
    try:
        image = cv2.imread(image_dir)
        if image is not None:
            image = cv2.resize(image, default_image_size)
            return img_to_array(image)
        else:
            return np.array([])
    except Exception as e:
        print(f"Error : {e}")
        return None


image_list, label_list = [], []
try:
    print("[INFO] Loading images ...")
    root_dir = listdir(directory_root)
    for directory in root_dir:
        # remove .DS_Store from list
        if directory == ".DS_Store":
            root_dir.remove(directory)

    for plant_folder in root_dir:
        plant_disease_folder_list = listdir(f"{directory_root}/{plant_folder}")

        for disease_folder in plant_disease_folder_list:
            # remove .DS_Store from list
            if disease_folder == ".DS_Store":
                plant_disease_folder_list.remove(disease_folder)

        for plant_disease_folder in plant_disease_folder_list:
            print(f"[INFO] Processing {plant_disease_folder} ...")
            plant_disease_image_list = listdir(f"{directory_root}/{plant_folder}/{plant_disease_folder}/")

            for single_plant_disease_image in plant_disease_image_list:
                if single_plant_disease_image == ".DS_Store":
                    plant_disease_image_list.remove(single_plant_disease_image)

            for image in plant_disease_image_list:
                image_directory = f"{directory_root}/{plant_folder}/{plant_disease_folder}/{image}"
                if image_directory.endswith(".jpg") == True or image_directory.endswith(".JPG") == True:
                    image_list.append(convert_image_to_array(image_directory))
                    label_list.append(plant_disease_folder)
    print("[INFO] Image loading completed")
except Exception as e:
    print(f"Error : {e}")
image_size = len(image_list)
print(image_size)
label_binarizer = LabelBinarizer()
image_labels = label_binarizer.fit_transform(label_list)
pickle.dump(label_binarizer, open('custom_tomato_label_transform.pkl', 'wb'))
n_classes = len(label_binarizer.classes_)
print(label_binarizer.classes_)
model = Sequential()
inputShape = (img_height, img_width, depth)
chanDim = -1
if K.image_data_format() == "channels_first":
    inputShape = (depth, img_height, img_width)
    chanDim = 1
model.add(Conv2D(32, (3, 3), padding="same", input_shape=inputShape))
model.add(Activation('relu'))
model.add(BatchNormalization(axis=chanDim))
model.add(MaxPooling2D(pool_size=(3, 3)))
model.add(Dropout(0.25))
model.add(Conv2D(64, (3, 3), padding="same"))
model.add(Activation('relu'))
model.add(BatchNormalization(axis=chanDim))
model.add(Conv2D(64, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=chanDim))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(128, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=chanDim))
model.add(Conv2D(128, (3, 3), padding="same"))
model.add(Activation("relu"))
model.add(BatchNormalization(axis=chanDim))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(1024))
model.add(Activation("relu"))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Dense(n_classes))
model.add(Activation("softmax"))
model.summary()
opt = Adam(lr=INIT_LR, decay=INIT_LR / epochs)
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)
validation_datagen = ImageDataGenerator(rescale=1. / 255)
train = train_datagen.flow_from_directory('D:/Official purpose/Sprint - 27/Custom_dataset_for_tomato/train',
                                                    target_size=(img_width, img_height),
                                                    batch_size=batch_size, class_mode='categorical')
validation = validation_datagen.flow_from_directory(
    'D:/Official purpose/Sprint - 27/Custom_dataset_for_tomato/validation',
    target_size=(img_width, img_height),
    batch_size=batch_size, class_mode='categorical')
history = model.fit(train,
                    steps_per_epoch=nb_train_samples // batch_size,
                    epochs=epochs, validation_data=validation,
                    validation_steps=nb_validation_samples // batch_size)
model.save('custom_tomato_model.h5')
accuracy = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(accuracy)+1)
plt.plot(epochs, accuracy, 'b', label='Training accuracy')
plt.plot(epochs, val_acc, 'r', label='Validation accuracy')
plt.title('Training and Validation accuracy')
plt.legend()
plt.figure()
plt.plot(epochs, loss, 'b', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and Validation loss')
plt.legend()
plt.show()
print(accuracy, val_acc, loss, val_loss)
loaded_model =load_model('custom_tomato_model.h5')
model_disease = loaded_model
image_dir = "D:/Official purpose/Sprint - 26/Crop images/Tomato_Leaf_Mold.JPG"
img = plt.imread('D:/Official purpose/Sprint - 26/Crop images/Tomato_Leaf_Mold.JPG')
im = convert_image_to_array(image_dir)
np_image_li = np.array(im, dtype=np.float16) / 255
npp_image = np.expand_dims(np_image_li, axis=0)
result = model_disease.predict(npp_image)
print(result)
itemindex = np.where(result == np.max(result))
print("probability:" + str(np.max(result)) + "\n" + label_binarizer.classes_[itemindex[1][0]])
plt.imshow(img)
plt.show()
