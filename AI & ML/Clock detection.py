import cv2
clock_cascade = cv2.CascadeClassifier('D:/Anaconda/opencv/sources/data/haarcascades/classifier WallClock.xml')
img = cv2.imread('clocks.jpg')


def detect_clock(img):
    clock = clock_cascade.detectMultiScale(img, 1.15, 4)
    for (x, y, w, h) in clock:
        cv2.rectangle(img, (x, y), (x+w, y+h), color=(0, 255, 0), thickness=2)
    return img


clock_frame = detect_clock(img)
cv2.imshow('img', clock_frame)
cv2.waitKey(0)
