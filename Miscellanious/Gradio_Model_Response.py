import gradio as gr
import tensorflow as tf
import numpy as np
import requests
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.models import load_model
model = load_model("E:/Official purpose/Sprint - 8/Final_Mango_Model_S8.h5")
class_names = ['Anthracnose', 'cant_recognise_click_again', 'Dieback Formation', 'Gummosis','Healthy Condition', 'Malformation', 'Mealybug Attack', 'Powdery mildew']


def example(image):
    image = image.reshape((-1, 224, 224, 3))
    image = tf.keras.applications.inception_v3.preprocess_input(image)
    prediction = model.predict(image).flatten()
    return {class_names[i]: float(prediction[i]) for i in range(8)}


# initializing the input component
image = gr.inputs.Image(shape = (224, 224))
# initializing the output component
label = gr.outputs.Label(num_top_classes = 8)
# launching the interface
gr.Interface(fn = example,inputs = image,outputs = label,capture_session = True, title="Model Deploy",description= "Description of the user interface").launch(share=True)
