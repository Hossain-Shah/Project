from imageai.Prediction import ImagePrediction
import os
prediction = ImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath("C:/Users/HP/Downloads/resnet50_weights_tf_dim_ordering_tf_kernels.h5")
prediction.loadModel()
predictions, percentage_probabilities = prediction.predictImage("F:/Photos/Campus life(Tangail)/IMG_20181010_165555.jpg", result_count=5)
for index in range(len(predictions)):
    print(predictions[index] , " : " , percentage_probabilities[index])
