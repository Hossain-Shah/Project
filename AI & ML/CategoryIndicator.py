import numpy as np
import cv2
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D
from keras.optimizers import Adam
from keras.layers import MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
train_dir = 'D:/Pycharm/Program/AI_Stat_ANN/AttractionLevelDataset/train'
val_dir = 'D:/Pycharm/Program/AI_Stat_ANN/AttractionLevelDataset/test'
train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(48,48),
        batch_size=2,
        color_mode="grayscale",
        class_mode='categorical')
validation_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(48,48),
        batch_size=2,
        color_mode="grayscale",
        class_mode='categorical')
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))
model.compile(loss='binary_crossentropy',optimizer=Adam(lr=0.0001, decay=1e-6),metrics=['accuracy'])
model_info = model.fit_generator(
        train_generator,
        steps_per_epoch=8 // 2,
        epochs=2,
        validation_data=validation_generator,
        validation_steps=6 // 2)
model.save_weights('category_model.h5')
cv2.ocl.setUseOpenCL(False)
dict = {0: "attractive", 1: "less_attractive"}
img = cv2.imread('F:/Photos/Friends & Family(Dhaka)/received_1816118352028837.jpeg')
r = 500.0 / img.shape[1]
dim = (500, int(img.shape[0] * r))
resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
bounding_box = cv2.CascadeClassifier('D:/Anaconda/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
num_faces = bounding_box.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5)
for (x, y, w, h) in num_faces:
    cv2.rectangle(resized, (x, y - 50), (x + w, y + h + 10), (255, 0, 0), 2)
    roi_gray = gray[y:y + h, x:x + w]
    cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
    category_prediction = model.predict(cropped_img)
    maxindex = int(np.argmax(category_prediction))
    cv2.putText(resized, dict[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
cv2.imshow('Image', cv2.resize(resized,(1200,860),interpolation = cv2.INTER_CUBIC))
cv2.waitKey(0)
