from imageai.Prediction.Custom import CustomImagePrediction
import os
prediction = CustomImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath("C:/Users/HP/Downloads/idenprof/models/idenprof_061-0.7933.h5")
prediction.setJsonPath("C:/Users/HP/Downloads/idenprof/json/model_class.json")
prediction.loadModel(num_objects=10)

predictions, probabilities = prediction.predictImage("F:/Photos/Me/20180317_004709.jpg", result_count=3)

for eachPrediction, eachProbability in zip(predictions, probabilities):
    print(eachPrediction , " : " , eachProbability)