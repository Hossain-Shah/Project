from imageai.Detection import VideoObjectDetection
import os
import cv2
camera = cv2.VideoCapture(0)
detector = VideoObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join("C:/Users/HP/Downloads/yolo.h5"))
detector.loadModel()
video_path = detector.detectObjectsFromVideo(camera_input=camera,output_file_path=os.path.join("camera_detected_1"), frames_per_second=29, log_progress=True)

