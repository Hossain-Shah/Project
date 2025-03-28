from imageai.Detection import VideoObjectDetection
import os
detector = VideoObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join("C:/Users/HP/Downloads/yolo.h5"))
detector.loadModel()
video_path = detector.detectObjectsFromVideo(input_file_path=os.path.join(""),output_file_path=os.path.join("Output_lost"), frames_per_second=29, log_progress=True)
