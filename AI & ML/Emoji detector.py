import numpy as np
import cv2
from keras.models import load_model
cv2.ocl.setUseOpenCL(False)
EMOTIONS = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
emotion_model = 'C:/Users/HP/Downloads/_mini_XCEPTION.106-0.65.hdf5'
img = cv2.imread('F:/Photos/Campus life(Tangail)/17321359_1683060555327445_1861456474_n.jpg')
r = 500.0 / img.shape[1]
dim = (500, int(img.shape[0] * r))
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
bounding_box = cv2.CascadeClassifier('D:/Anaconda/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
gray_frame = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
emotion_classifier = load_model(emotion_model, compile=False)
faces = bounding_box.detectMultiScale(gray_frame,scaleFactor=1.3, minNeighbors=5)
for (x, y, w, h) in faces:
    cv2.rectangle(resized, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
    roi_gray_frame = gray_frame[y:y + h, x:x + w]
    cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (48, 48)), -1), 0)
    emotion_prediction = emotion_classifier.predict(cropped_img)
    maxindex = int(np.argmax(emotion_prediction))
    cv2.putText(resized, EMOTIONS[maxindex], (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
cv2.imshow('Video', cv2.resize(resized,(1200,860),interpolation = cv2.INTER_CUBIC))
cv2.waitKey(0)
