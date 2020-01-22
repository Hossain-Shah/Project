import cv2
import imutils
import time
import numpy as np

img = cv2.imread('F:/Photos/Campus life(Tangail)/17321359_1683060555327445_1861456474_n.jpg')
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
gender_list = ['Male', 'Female']


def initialize_caffe_models():
    age_net = cv2.dnn.readNetFromCaffe('C:/Users/HP/Downloads/Compressed/age_deploy.prototxt','C:/Users/HP/Downloads/age_net.caffemodel')
    gender_net = cv2.dnn.readNetFromCaffe('C:/Users/HP/Downloads/Compressed/gender_deploy.prototxt','C:/Users/HP/Downloads/gender_net.caffemodel')
    return (age_net, gender_net)


def read_from_img(age_net, gender_net):
    font = cv2.FONT_HERSHEY_SIMPLEX
    while True:
        face_cascade = cv2.CascadeClassifier('D:/Anaconda/opencv/sources/data/haarcascades/haarcascade_frontalface_alt.xml')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
        if (len(faces) > 0):
            print("Found {} faces".format(str(len(faces))))
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
                face_img = img[y:y + h, h:h + w].copy()
                blob = cv2.dnn.blobFromImage(face_img, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
                gender_net.setInput(blob)
                gender_preds = gender_net.forward()
                gender = gender_list[gender_preds[0].argmax()]
                print("Gender : " + gender)
                age_net.setInput(blob)
                age_preds = age_net.forward()
                age = age_list[age_preds[0].argmax()]
                print("Age Range: " + age)
                overlay_text = "%s %s" % (gender, age)
                cv2.putText(img, overlay_text, (x, y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow('frame', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break


if __name__ == "__main__":
    age_net, gender_net = initialize_caffe_models()
    read_from_img(age_net, gender_net)
