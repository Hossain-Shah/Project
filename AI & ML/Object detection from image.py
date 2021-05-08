from imageai.Detection import ObjectDetection
import os
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join("C:/Users/HP/Downloads/resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()
detections = detector.detectObjectsFromImage(input_image=os.path.join("F:/Photos/Campus life(Tangail)/IMG_20180404_174403.jpg"),output_image_path=os.path.join("D:/Pycharm/Program/AI_Stat_ANN/detection.jpg"))
for eachObject in detections:
    print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
detections, extracted_images = detector.detectObjectsFromImage(input_image=os.path.join("F:/Photos/Campus life(Tangail)/IMG_20180404_174403.jpg"), output_image_path=os.path.join("D:/Pycharm/Program/AI_Stat_ANN/detection.jpg"), extract_detected_objects=True)
