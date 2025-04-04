from keras.preprocessing.image import img_to_array
import imutils
import cv2
from keras.models import load_model
import numpy as np
import pandas as pd
import datetime
# parameters for loading data and images
detection_model_path = 'E:/Official purpose/Sprint - 4/haarcascade_frontalface_default.xml'
emotion_model_path = 'E:/Official purpose/Sprint - 4/_mini_XCEPTION.106-0.65.hdf5'
# hyper-parameters for bounding boxes shape
# loading models
face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]
# starting video streaming
cv2.namedWindow('my_face', cv2.WND_PROP_FULLSCREEN)
camera = cv2.VideoCapture(0)
while True:
    ret, frame = camera.read()
    # reading the frame
    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameClone = frame.copy()
    faces = face_detection.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
    for (x, y, w, h) in faces:
        cv2.rectangle(frameClone, (x, y), (x + w, y + h), (255, 255, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frameClone[y:y + h, x:x + w]
        roi = gray[y:y + h, x:x + w]
        roi = cv2.resize(roi, (48, 48))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        preds = emotion_classifier.predict(roi)[0]
        emotion_probability = np.max(preds)
        label = EMOTIONS[preds.argmax()]
        cv2.putText(frameClone, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 0), 2)
    canvas = np.zeros((250, 300, 3), dtype="uint8")
    if len(faces) > 0:
        faces = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (fX, fY, fW, fH) = faces
        # Extract the ROI of the face from the grayscale image, resize it to a fixed 48x48 pixels, and then prepare
        # the ROI for classification via the CNN
        roi = gray[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (48, 48))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        preds = emotion_classifier.predict(roi)[0]
        emotion_probability = np.max(preds)
        label = EMOTIONS[preds.argmax()]
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        f = open("sentiment_analysis_report.csv", "w")
        f.write("{}\n".format("DATE AND TIME"))
        for y in dt_string:
            f.write("{}".format(y[0]))
        f.write("\n{},{}\n".format("EMOTION", "PERCENTAGE"))
        for x in zip(EMOTIONS, preds):
            f.write("{},{}\n".format(x[0], x[1]))
        f.close()
        for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
            text = "{}: {:.2f}%".format(emotion, prob * 100)
            w = int(prob * 300)
            cv2.rectangle(canvas, (7, (i * 35) + 5), (w, (i * 35) + 35), (0, 0, 255), -1)
            cv2.putText(canvas, text, (10, (i * 35) + 23), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
            cv2.putText(frameClone, label, (fX, fY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH), (0, 0, 255), 2)
            cv2.imshow('my_face', frameClone)
        cv2.imshow("Probabilities", canvas)
        cv2.waitKey(1) & 0xFF
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # if we are using a webcam, release the pointer
camera.release()
cv2.destroyAllWindows()