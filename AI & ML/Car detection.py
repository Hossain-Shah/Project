import cv2
car_cascade = cv2.CascadeClassifier('D:/Anaconda/opencv/build/etc/haarcascades/haarcascade_car.xml')
img = cv2.imread('Laned_street.jpg')


def detect_cars(img):
    cars = car_cascade.detectMultiScale(img, 1.15, 4)
    for (x, y, w, h) in cars:
        cv2.rectangle(img, (x, y), (x+w, y+h), color=(0, 255, 0), thickness=2)
    return img


cars_frame = detect_cars(img)
cv2.imshow('img', cars_frame)
cv2.waitKey(0)
