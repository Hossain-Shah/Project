from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import pickle
import numpy as np
img = image.load_img('D:/Official purpose/Sprint - 26/Crop images/Tomato_Leaf_Mold.JPG', target_size=(224, 224))
img = image.img_to_array(img)
img = np.expand_dims(img, axis=0)
img = img/255
model_file = 'D:/Official purpose/Sprint - 29/tomato_model_resnet50.h5'
saved_classifier_model = load_model(model_file)
prediction = saved_classifier_model.predict(img)
label_binarizer = pickle.load(open('D:/Official purpose/Sprint - 27/custom_tomato_label_transform.pkl','rb'))
print({label_binarizer.inverse_transform(prediction)[0]})
