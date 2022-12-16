#Importing libraries
from detecto import core, utils, visualize

#Inputting test image
image = utils.read_image('images/dog/n02085620_574.jpg')

#Initializes a pre-trained model
model = core.Model()

#Evaluating model
labels, boxes, scores = model.predict_top(image)

#Outputting predictions
visualize.show_labeled_image(image, boxes, labels)
print(labels, boxes, scores)
