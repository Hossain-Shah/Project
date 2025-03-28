import os
import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import models
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.python.keras import utils
current_path = os.getcwd()
# getting the current path
category_path = os.path.join(current_path, 'static\yolo.pkl')
# loading class_to_num_category
predictor_model = load_model(r'static\yolov3.h5')
with open(category_path, 'rb') as handle:
    category = pickle.load(handle)
# loading the feature extractor model
class_dict = {'Crop': 0, 'Weed': 1}
class_names = list(class_dict.keys())


def predictor(img_path): # here image is file name
    img = load_img(img_path, target_size=(224, 224))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    #features = category.predict(img)
    prediction = predictor_model.predict(img)
    #prediction = pd.DataFrame(np.round(prediction, 1), columns=category).transpose()
    #prediction.columns = ['values']
    #prediction = prediction.nlargest(5, 'values')
    #prediction = prediction.reset_index()
    #prediction.columns = ['name', 'values']
    prediction = prediction.flatten()
    m = max(prediction)
    for index, item in enumerate(prediction):
        if item == m:
            result = class_names[index]
            print(result)
    return(result)


#importing all the helper fxn from helper.py which we will create later
import streamlit as st
import os
import matplotlib.pyplot as plt
import seaborn as sns
import json
sns.set_theme(style="darkgrid")
sns.set()
from PIL import Image
st.title('Classifier')


def save_uploaded_file(uploaded_file):
    try:
        with open(os.path.join('static/images', uploaded_file.name), 'wb') as f:
            f.write(uploaded_file.getbuffer())
        return 1
    except:
        return 0


uploaded_file = st.file_uploader("Upload Image")
# text over upload button "Upload Image"
if uploaded_file is not None:
    if save_uploaded_file(uploaded_file):
        # display the image
        display_image = Image.open(uploaded_file)
        st.image(display_image)
        prediction = predictor(os.path.join('static/images', uploaded_file.name))
        os.remove('static/images/'+uploaded_file.name)
        # deleting uploaded saved picture after prediction
        # drawing graphs
        st.text('Predictions :-')
        fig, ax = plt.subplots()
        ax = sns.barplot(data=prediction)
        ax.set(xlabel='Confidence %', ylabel='Label')
        st.pyplot(fig)

