import torch
from detecto import core, utils, visualize
from detecto.visualize import show_labeled_image, plot_prediction_grid
from torchvision import transforms
import matplotlib.pyplot as plt
import numpy as np
custom_transforms = transforms.Compose([
transforms.ToPILImage(),
transforms.Resize(900),
transforms.RandomHorizontalFlip(0.5),
transforms.ColorJitter(saturation=0.2),
transforms.ToTensor(),
utils.normalize_transform(),
])
Train_dataset=core.Dataset('D:/WorkSpace/Q3S7/Pytorch Detecto model training/Paddy/train/images/',transform=custom_transforms)
Validation_dataset = core.Dataset('D:/WorkSpace/Q3S7/Pytorch Detecto model training/Paddy/validation/images/')
print(Train_dataset, Validation_dataset)
loader=core.DataLoader(Train_dataset, batch_size=2, shuffle=True)
model = core.Model(['Blast', 'False_Smut', 'RiceBug', 'SheathRot', 'StemBorer', 'unrelated_image'])
losses = model.fit(loader, Validation_dataset, epochs=25, lr_step_size=5, learning_rate=0.001, verbose=True)
plt.plot(losses)
plt.show()
model.save('D:/WorkSpace/Q3S7/Pytorch Detecto model training/rice_faster_rcnn_detecto.pth')
model = core.Model.load('D:/WorkSpace/Q3S7/Pytorch Detecto model training/rice_faster_rcnn_detecto.pth', ['Blast', 'False_Smut', 'RiceBug', 'SheathRot', 'StemBorer', 'unrelated_image'])
image = utils.read_image('D:/WorkSpace/Q3S6/Crop images/rice_blast_233754632_1732789123577441_6836549985591341373_n.jpg') 
predictions = model.predict(image)
labels, boxes, scores = predictions
show_labeled_image(image, boxes, labels)
thresh=0.6
filtered_indices=np.where(scores>thresh)
filtered_scores=scores[filtered_indices]
filtered_boxes=boxes[filtered_indices]
num_list = filtered_indices[0].tolist()
filtered_labels = [labels[i] for i in num_list]
show_labeled_image(image, filtered_boxes, filtered_labels)
