import datetime
import pickle
import json
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from PlantDiseasePestRecognizer.settings import BASE_DIR
from keras.preprocessing import image
import numpy as np
from keras.models import load_model
class_dict = {'Apple___Apple_scab': 0,
            'Apple___Black_rot': 1,
            'Apple___Cedar_apple_rust': 2,
            'Apple___healthy': 3,
            'Blueberry___healthy': 4,
            'Cherry_(including_sour)___Powdery_mildew': 5,
            'Cherry_(including_sour)___healthy': 6,
            'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': 7,
            'Corn_(maize)___Common_rust_': 8,
            'Corn_(maize)___Northern_Leaf_Blight': 9,
            'Corn_(maize)___healthy': 10,
            'Grape___Black_rot': 11,
            'Grape___Esca_(Black_Measles)': 12,
            'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': 13,
            'Grape___healthy': 14,
            'Orange___Haunglongbing_(Citrus_greening)': 15,
            'Peach___Bacterial_spot': 16,
            'Peach___healthy': 17,
            'Pepper,_bell___Bacterial_spot': 18,
            'Pepper,_bell___healthy': 19,
            'Potato___Early_blight': 20,
            'Potato___Late_blight': 21,
            'Potato___healthy': 22,
            'Raspberry___healthy': 23,
            'Soybean___healthy': 24,
            'Squash___Powdery_mildew': 25,
            'Strawberry___Leaf_scorch': 26,
            'Strawberry___healthy': 27,
            'Tomato___Bacterial_spot': 28,
            'Tomato___Early_blight': 29,
            'Tomato___Late_blight': 30,
            'Tomato___Leaf_Mold': 31,
            'Tomato___Septoria_leaf_spot': 32,
            'Tomato___Spider_mites Two-spotted_spider_mite': 33,
            'Tomato___Target_Spot': 34,
            'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 35,
            'Tomato___Tomato_mosaic_virus': 36,
            'Tomato___healthy': 37}

class_names = list(class_dict.keys())

@api_view(['GET'])
def __index__function(request):
    start_time = datetime.datetime.now()
    elapsed_time = datetime.datetime.now() - start_time
    elapsed_time_ms = (elapsed_time.days * 86400000) + (elapsed_time.seconds * 1000) + (elapsed_time.microseconds / 1000)
    return_data = {
        "error" : "0",
        "message" : "Successful",
        "restime" : elapsed_time_ms
    }
    return HttpResponse(json.dumps(return_data), content_type='application/json; charset=utf-8')

@api_view(['POST','GET'])
def predict_plant_disease(request):
    try:
        if request.method == "GET" :
            return_data = {
                "error" : "0",
                "message" : "Plant Disease Recognition Api"
            }
        else:
            if request.method == 'POST' and request.FILES['myfile']:
                post = request.method == 'POST'
                myfile = request.FILES['myfile']
                img = image.load_img(myfile, target_size=(224, 224))
                img = image.img_to_array(img)
                img = np.expand_dims(img, axis=0)
                img = img/255
                model_file = f"{BASE_DIR}/ml_files/AlexNetModel.hdf5"
                saved_classifier_model = load_model(model_file)
                prediction = saved_classifier_model.predict(img)
                prediction = prediction.flatten()
                m = max(prediction)
                for index, item in enumerate(prediction):
                    if item == m:
                        result = class_names[index]
                return_data = {
                    "error" : "0",
                    "data" : f"{result}"
                }
            else :
                return_data = {
                    "error" : "1",
                    "message" : "Request Body is empty"
                }
    except Exception as e:
        return_data = {
            "error" : "3",
            "message" : f"Error : {str(e)}",
        }
    return HttpResponse(json.dumps(return_data), content_type='application/json; charset=utf-8')

