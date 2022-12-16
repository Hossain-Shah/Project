#Importing libraries
from detecto import core, utils
from detecto.visualize import show_labeled_image, plot_prediction_grid
from torchvision import transforms
import matplotlib.pyplot as plt
import numpy as np

#Image augmentation
custom_transforms = transforms.Compose([
transforms.ToPILImage(),
transforms.Resize(900),
transforms.RandomHorizontalFlip(0.5),
transforms.ColorJitter(saturation=0.2),
transforms.ToTensor(),
utils.normalize_transform(),
])

#Model training
Train_dataset = core.Dataset('images/', transform=custom_transforms)#L1
Test_dataset = core.Dataset('images/')#L2
loader = core.DataLoader(Train_dataset, batch_size=2, shuffle=True)#L3
model = core.Model(['dog'])#L4
losses = model.fit(loader, Test_dataset, epochs=25, lr_step_size=5, learning_rate=0.001, verbose=True)#L5

#Model saving
model.save('custom_model_weights.pth')


#Inputting test image
image = utils.read_image('images/dog/n02085620_574.jpg')

#Initializes the trained model
model = core.Model.load('custom_model_weights.pth', ['dog'])

#Evaluating model
labels, boxes, scores = model.predict_top(image)

#Outputting predictions
show_labeled_image(image, boxes, labels)
print(labels, boxes, scores)
plt.plot(losses)
plt.show()
