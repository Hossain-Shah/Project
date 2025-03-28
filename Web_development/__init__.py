# -*- coding: utf-8 -*-
import logging
import os
import sqlite3
import sys
from datetime import datetime
import math 
import random
from types import coroutine
import numpy as np
from numpy.lib.function_base import insert
import phonenumbers
import tensorflow as tf
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from numpy.core import records
from PIL import Image
from sqlalchemy import create_engine
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.python.eager.context import device
 
logging.basicConfig(
    filename='record.log',
    level=logging.DEBUG,
    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
    )

DB_PATH = "dr_geneticaapi.db"
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
api = Api(app)
API_KEY_GLOBAL = "^)@$!"

parser = reqparse.RequestParser()

def get_models_prediction(crop_id, image_path):
    # here the dictionary represents the crop id of the crop and the model path of the crop
    # crops_model_path = { mango's crop id : model path }
    crops_model_path = {1: "Mango_Model.h5", 2: "Dragon_Model.h5", 3: "Citrus_Model.h5"}

    # mango_disease_id_map = { model_disease_id : [database_disease_id, disease_name] }
    mango_disease_id_map = {
        0: [26, "seems unrelated"],
        1: [1, "anthracnose"],
        2: [2, "dieback formation"],
        3: [5, "malformation"],
        4: [6, "mealybug attack"],
        5: [3, "gummosis"],
        6: [7, "powdery mildew"],
        7: [4, "healthy condition"],
        8: [21, "can't recognize"],
    }

    # dragon_fruit_disease_id_map = { model_disease_id : [database_disease_id, disease_name] }
    dragon_fruit_disease_id_map = {
        0: [27, "seems unrelated"],
        1: [10, "branch rot damage"],
        2: [9, "root rot damage"],
        3: [11, "rotten dragon fruit"],
        4: [25, "fresh condition"],
        5: [24, "good fruit"],
        6: [8, "noticeable ant attack"],
        7: [22, "can't recognize"],
    }
    
    # citrus_fruit_disease_id_map = { model_disease_id : [database_disease_id, disease_name] }
    citrus_fruit_disease_id_map = {
        0: [28, "seems unrelated"],
        1: [16, "boron deficiency"],
        2: [18, "canker diseases"],
        3: [12, "caterpillar damage"],
        4: [14, "leaf miner"],
        5: [17, "hlb symptoms"],
        6: [19, "scab disease"],
        7: [13, "white fly"],
        8: [15, "zinc deficiency"],
        9: [23, "can't recognize "],
    }

    # disease_id_map = { crop_id : crop_disease_id_map }
    disease_id_map = {
        1: mango_disease_id_map,
        2: dragon_fruit_disease_id_map,
        3: citrus_fruit_disease_id_map,
    }

    # load the model
    model = load_model(crops_model_path[int(crop_id)])
    img = image.load_img(image_path, target_size=(299, 299))
    image_array = image.img_to_array(img)
    image_array = image_array / 255
    image_array = np.expand_dims(image_array, axis=0)
    model_preds = model.predict(image_array)
    model_predition = np.argmax(model_preds, axis=1)
    # getting the predicted id and accuracy from the model
    model_predicted_disease_id = model_predition[0].item()
    accuracy = model_preds[0][model_predicted_disease_id]
    disease_id_of_database = disease_id_map[int(crop_id)][model_predicted_disease_id][0]
    # get disease information from disease table in database

    sql = f"""
    SELECT 
        ifnull(id, '') as disease_id, 
        ifnull(crop_id, '') as crop_id, 
        ifnull(en_name, '') as en_name, 
        ifnull(bn_name, '') as bn_name, 
        ifnull(en_details, '') as en_details, 
        ifnull(bn_details,'') as bn_details ,
        ifnull(detection_type,'') as detection_type 
    from diseases where id = {disease_id_of_database};"""
    connection=sqlite3.connect(DB_PATH)
    cursor=connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()

    columns = [column[0] for column in cursor.description]
    result_dict = dict(zip(columns, result))

    result_dict["accuracy"] = float(accuracy)
    return result_dict

s = ""
class DiseaseDetectionInformation(Resource):
    def __init__(self):
        self.img_dir = os.path.join(os.getcwd(), "static")
        if not os.path.exists(self.img_dir):
            os.makedirs(self.img_dir)

    def get(self):
        return s

    def post(self):
        parser.add_argument("api_key", type=str)
        parser.add_argument("user_id", type=int)
        parser.add_argument("lat", type=str)
        parser.add_argument("lon", type=str)
        parser.add_argument("crop_id", type=int)
        args = parser.parse_args()

        
        lat = None
        lon = None
        crop_id = None
        image_as_string = None
        data = {}
        
        lat = args["lat"]
        lon = args["lon"]
        crop_id = args["crop_id"]
        api_key = args["api_key"]
        user_id = args["user_id"]
        image_as_string = request.files["image"].stream
        img = Image.open(image_as_string)
        
        if (
            user_id is None
            or image_as_string is None
            or api_key is None
            or img is None
            or crop_id is None
        ):
            message = "User Id, Image, Crop Id and Api Key are required"
            message_bn = "ব্যবহারকারীর আইডি, চিত্র এবং এপিআই প্রয়োজন"
            code = "4000"
            status = "error"

        elif api_key != API_KEY_GLOBAL:
            message = "Api key not matched"
            code = "4000"
            status = "error"
            message_bn = "এপি আই কী মিলছে না"
           
        else:
            created_time = datetime.now()
            updated_time = datetime.now()

            created_time_str = created_time.strftime("%Y-%m-%d %H:%M:%S")
            updated_time_str = updated_time.strftime("%Y-%m-%d %H:%M:%S")
            connection=sqlite3.connect(DB_PATH)
            cursor=connection.cursor()
            cursor.execute("SELECT max(id) from disease_histories;")
            last_inserted_id = cursor.fetchone()
            last_inserted_id = last_inserted_id[0]

            # image_as_string = request.files['image'].stream
            img = Image.open(image_as_string)

            # This condition is for empty disease_histories table
            if last_inserted_id is None:
                last_inserted_id = 0
            else:
                last_inserted_id = last_inserted_id + 1
            file_name = "image" + str(last_inserted_id + 1) + ".jpg"

            file_path = os.path.join(self.img_dir, file_name)
            img.save(file_path, "jpeg")

            message = "Successfully Detected"
            message_bn = "ছবি সফলভাবে সনাক্ত করা হয়েছে "
            code = "2000"
            status = "success"

            image_path = "https://api.drchashi.com/static/" + file_name
            # changes starts here
            disease_information = get_models_prediction(str(crop_id), file_path)
            sql ="""
                insert into disease_histories(
                    user_id, crop_id, disease_id, 
                    image, name, bn_name, 
                    accuracy, details, bn_details, 
                    detection_type, lat, lon, 
                    created_time, updated_time, status) 
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
            cursor.execute(
            sql,
            (
                user_id,
                crop_id,
                disease_information["disease_id"],
                image_path,
                disease_information["en_name"],
                disease_information["bn_name"],
                disease_information["accuracy"],
                disease_information["en_details"],
                disease_information["bn_details"],
                disease_information["detection_type"],
                lat,
                lon,
                created_time_str,
                updated_time_str,
                1,
            ),
            )

            if lat is None or lon is None:
                nearest_delear = []
            else:
                nearest_delear = get_top_five_nearest_dealers(lat, lon)
            
            if disease_information["detection_type"] == "disease":
                data = {
                    "en_name": disease_information["en_name"],
                    "bn_name": disease_information["bn_name"],
                    "accuracy": disease_information["accuracy"],
                    "en_details": disease_information["en_details"],
                    "bn_details": disease_information["bn_details"],
                    "id": last_inserted_id,
                    "image": image_path,
                    "disease_id": disease_information["disease_id"],
                    "date_time": created_time_str,
                    "detection_type": disease_information["detection_type"],
                    "crop_id": disease_information["crop_id"],
                    "recommended_solutions": get_recommended_solutions(
                        disease_information["disease_id"]
                    ),
                    "nearest_dealers": nearest_delear,
                }
            else:
                data = {
                    "en_name": disease_information["en_name"],
                    "bn_name": disease_information["bn_name"],
                    "accuracy": disease_information["accuracy"],
                    "en_details": disease_information["en_details"],
                    "bn_details": disease_information["bn_details"],
                    "id": last_inserted_id,
                    "image": image_path,
                    "disease_id": disease_information["disease_id"],
                    "date_time": created_time_str,
                    "detection_type": disease_information["detection_type"],
                    "crop_id": disease_information["crop_id"],
                    "recommended_solutions": [],
                    "nearest_dealers": [],
                }
        
        return jsonify(
            message=message, message_bn=message_bn, code=code, status=status, data=data
        )

class Customers(Resource):
    def post(self):
        parser_s = reqparse.RequestParser()
        parser_s.add_argument("api_key", type=str)
        parser_s.add_argument("customer_id", type=int)

        args = parser_s.parse_args()
        api_key = args["api_key"]
        customer_id = args["customer_id"]
        list = {}

        if customer_id is None or not customer_id:
            message = "Customer Id is required"
            message_bn = "গ্রাহক আইডি আবশ্যক"
            code = "4000"
            status = "error"
            

       
        elif api_key != API_KEY_GLOBAL:
            message = "Api key not matched"
            code = "4000"
            status = "error"
            message_bn = "এপি আই কী মিলছে না"
            
        else:
            connection=sqlite3.connect(DB_PATH)
            cursor=connection.cursor()
            cursor.execute(
                f"""
                select
                    ifnull(en_about_us, '') as en_about_us,
                    ifnull(en_help_line, '') as en_help_line,
                    ifnull(en_home_title, '') as en_home_title,
                    ifnull(bn_about_us, '') as bn_about_us,
                    ifnull(bn_help_line, '') as bn_help_line,
                    ifnull(bn_home_title, '') as bn_home_title,
                    ifnull(created_time, '') as created_time,
                    ifnull(updated_time, '') as updated_time,
                    ifnull(status, '') as status,
                    bn_copy_right,
                    en_copy_right,
                    en_use_guide,
                    bn_use_guide,
                    company_logo,
                    en_helpline_message,
                    bn_helpline_message,
                    about_us_image,
                    en_disclaimer_detect_problem,
                    bn_disclaimer_detect_problem,
                    en_disclaimer_how_to_use,
                    bn_disclaimer_how_to_use
                from customers
                where id = {customer_id};
                """
            )

            list = cursor.fetchone()

            columns = [column[0] for column in cursor.description]
            list =     dict(zip(columns, list))
            
            if not list:
                message = "Customer not found"
                message_bn = "গ্রাহক খুঁজে পাওয়া যায়নি"
                code = "4000"
                status = "error"
            else:
                message = "Customer found"
                message_bn = "গ্রাহক খুঁজে পাওয়া গেছে"
                code = "2000"
                status = "success"

        return jsonify(
            message=message,
            message_bn=message_bn,
            code=code,
            status=status,
            data=list,
        )

class Crops(Resource):
    def post(self):
        parser_s = reqparse.RequestParser()
        parser_s.add_argument("api_key", type=str)
        args = parser_s.parse_args()
        api_key = args["api_key"]

        list = []
        if api_key != API_KEY_GLOBAL:
            message = "Api key not matched"
            code = "2000"
            status = "error"
            message_bn = "এপি আই কী মিলছে না"

        sql_query = f"""
            select ifnull(id, '') as id, 
            ifnull(image, '') as image,  
            ifnull(en_details, '') as en_details, 
            ifnull(en_name, '') as en_name, 
            ifnull(bn_details, '') as bn_details, 
            ifnull(bn_name, '') as bn_name, 
            ifnull(created_time, '') as created_time, 
            ifnull(updated_time, '') as updated_time, 
            ifnull(status, '') as status from crops;
            """
        connection=sqlite3.connect(DB_PATH)
        cursor=connection.cursor()
        cursor.execute(sql_query)

        list = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        results = []
        for row in list:
            results.append(dict(zip(columns, row)))
        
        list = results

        if not list:
            message = "Crop information not  found"
            message_bn = "ফসলের তথ্য পাওয়া যায়নি"
            code = "4000"
            status = "error"
        else:
            message = "Crop information found"
            message_bn = "ফসলের তথ্য পাওয়া গেছে"
            code = "2000"
            status = "success"

        return jsonify(
            message=message,
            message_bn=message_bn,
            code=code,
            status=status,
            data=list,
        )

class SearchGuides(Resource):
    def post(self):
        parser_s = reqparse.RequestParser()
        parser_s.add_argument("api_key", type=str)
        parser_s.add_argument("disease_name", type=str)
        parser_s.add_argument("offset", type=int)
        parser_s.add_argument("limit", type=int)
        args = parser_s.parse_args()
        api_key = args["api_key"]
        disease_name = args["disease_name"]
        offset = args["offset"]
        limit = args["limit"]

        result = []

        if api_key != API_KEY_GLOBAL:
            message = "Api key not matched"
            code = "2000"
            status = "error"
            message_bn = "এপি আই কী মিলছে না"
            return jsonify(
                message=message,
                message_bn=message_bn,
                code=code,
                status=status,
                data=result,
            )

        if offset is None or limit is None or api_key is None:
            message = "Offset, Limit and Api Key are required"
            message_bn = "অফসেট, সীমাবদ্ধতা এবং এপিআই কী প্রয়োজন"
            code = "4000"
            status = "error"
            return jsonify(
                message=message,
                message_bn=message_bn,
                code=code,
                status=status,
                data=result,
            )
        connection=sqlite3.connect(DB_PATH)
        cursor=connection.cursor()
        if disease_name is None:
            cursor.execute(
                "select ifnull(id,'') as id , ifnull(image,'') as image, ifnull(accuracy,'') as accuracy, ifnull(en_details,'') as en_details, ifnull(en_name,'') as en_name, ifnull(bn_details,'') as bn_details, ifnull(bn_name,'') as bn_name, ifnull(created_time, '') as created_time, ifnull(updated_time, '') as updated_time, ifnull(status, '') as status from search_guides limit ?,?;",
                (offset, limit),
            )
        else:
            cursor.execute(
                "select ifnull(id,'') as id , ifnull(image,'') as image, ifnull(accuracy,'') as accuracy, ifnull(en_details,'') as en_details, ifnull(en_name,'') as en_name, ifnull(bn_details,'') as bn_details, ifnull(bn_name,'') as bn_name, ifnull(created_time, '') as created_time, ifnull(updated_time, '') as updated_time, ifnull(status, '') as status from search_guides where en_name like ? OR bn_name like ? limit ?,?;",
                ("%" + disease_name + "%", "%" + disease_name + "%", offset, limit),
            )

        list = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        results = []
        for row in list:
            results.append(dict(zip(columns, row)))
        
        list = results


        if not list:
            message = "Search guide information found"
            code = "4000"
            status = "error"
            message_bn = "সন্ধান গাইড তথ্য পাওয়া গেছে"

        else:
            message = "Search guide information not found"
            message_bn = "সন্ধান গাইড তথ্য পাওয়া যায়নি"
            code = "2000"
            status = "success"

        return jsonify(
            message=message,
            message_bn=message_bn,
            code=code,
            status=status,
            data=list,
        )

class Products(Resource):
    def post(self):
        parser_s = reqparse.RequestParser()
        parser_s.add_argument("offset", type=int)
        parser_s.add_argument("limit", type=int)
        parser_s.add_argument("product_name", type=str)
        parser_s.add_argument("api_key", type=str)

        args = parser_s.parse_args()

        offset = args["offset"]
        limit = args["limit"]
        product_name = args["product_name"]
        api_key = args["api_key"]

        if api_key != API_KEY_GLOBAL:
            message = "Api key not matched"
            code = "4000"
            status = "error"
            message_bn = "এপি আই কী মিলছে না"
        elif offset is None or limit is None:
            message = "Offset and Limit are required"
            message_bn = "অফসেট এবং সীমাবদ্ধতা প্রয়োজন"
            code = "4000"
            status = "error"  

        else:
            connection = sqlite3.connect(DB_PATH)
            cursor=connection.cursor()
            if product_name is None:
                cursor.execute(
                    "select ifnull(id, '') as id, ifnull(crop_id,'') as crop_id, 'https://api.drchashi.com/static/product_images/' ||  ifnull(image_name,'default.png') as image, ifnull(en_name,'') as en_name, ifnull(en_group,'') as en_group, ifnull(en_amount,'') as en_amount, ifnull(en_details,'') as en_details, ifnull(en_active_ingredients,'') as en_active_ingredients,  ifnull(en_mode_of_action,'') as en_mode_of_action, ifnull(bn_name,'') as bn_name, ifnull(bn_group,'') as bn_group, ifnull(bn_amount,'') as bn_amount, ifnull(bn_details, '') as bn_details,ifnull(bn_active_ingredients,'') as bn_active_ingredients, ifnull(bn_mode_of_action,'') as bn_mode_of_action, ifnull(disease_id,'') as disease_id, ifnull(group_name,'') as group_name from products limit ?,?;",
                    (offset, limit),
                )

            else:
                cursor.execute(
                    "select ifnull(id, '') as id, ifnull(crop_id,'') as crop_id, 'https://api.drchashi.com/static/product_images/' || ifnull(image_name,'default.png') as image, ifnull(en_name,'') as en_name, ifnull(en_group,'') as en_group, ifnull(en_amount,'') as en_amount, ifnull(en_details,'') as en_details, ifnull(en_active_ingredients,'') as en_active_ingredients,  ifnull(en_mode_of_action,'') as en_mode_of_action, ifnull(bn_name,'') as bn_name, ifnull(bn_group,'') as bn_group, ifnull(bn_amount,'') as bn_amount, ifnull(bn_details, '') as bn_details,ifnull(bn_active_ingredients,'') as bn_active_ingredients, ifnull(bn_mode_of_action,'') as bn_mode_of_action, ifnull(disease_id,'') as disease_id, ifnull(group_name,'') as group_name from products where en_name like ? OR bn_name like ? limit ?,?;",
                    ("%" + product_name + "%", "%" + product_name + "%", offset, limit),
                )

            list = cursor.fetchall()

            columns = [column[0] for column in cursor.description]
            results = []
            for row in list:
                results.append(dict(zip(columns, row)))
            
            list = results


            if not list:
                message = "Product Information not found"
                message_bn = "পণ্য তথ্য পাওয়া যায় নি"
                code = "4000"
                status = "error"

            else:
                message = "Product information found"
                message_bn = "পণ্য তথ্য পাওয়া  গেছে"
                code = "2000"
                status = "success"
        return jsonify(
            message=message,
            message_bn=message_bn,
            code=code,
            status=status,
            data=list,
        )

class SimilarProducts(Resource):
    def post(self):
        parser_s = reqparse.RequestParser()
        parser_s.add_argument("offset", type=int)
        parser_s.add_argument("limit", type=int)
        parser_s.add_argument("api_key", type=str)
        parser_s.add_argument("group_name", type=str)

        args = parser_s.parse_args()

        group_name = args["group_name"]
        offset = args["offset"]
        limit = args["limit"]
        api_key = args["api_key"]
        list = []
        if api_key != API_KEY_GLOBAL:
            message = "Api key not matched"
            message_bn = "এপি আই কী মিলছে না"
            code = "4000"
            status = "error"

        elif(offset is None or limit is None or api_key is None or group_name is None or not group_name):
            message = "Offset and Limit, Api Key and Group Name are required"
            message_bn = "অফসেট এবং সীমাবদ্ধতা, এপিআই কী এবং গোষ্ঠীর নাম প্রয়োজন"
            code = "4000"
            status = "error"
            
        else: 
            connection = sqlite3.connect(DB_PATH)
            cursor=connection.cursor()
            cursor.execute(
            "select ifnull(id,'') as id, 'https://api.drchashi.com/static/product_images/' || ifnull(image_name,'default.png') as image, ifnull(en_name,'') as en_name, ifnull(en_group,'') as en_group, ifnull(en_amount,'') as en_amount, ifnull(en_details,'') as en_details, ifnull(en_active_ingredients,'') as en_active_ingredients, ifnull(en_mode_of_action,'') as en_mode_of_action, ifnull(bn_name,'') as bn_name, ifnull(bn_group,'') as bn_group, ifnull(bn_amount,'') as bn_amount, ifnull(bn_details,'') as bn_details,ifnull(bn_active_ingredients,'') as bn_active_ingredients, ifnull(bn_mode_of_action,'') as bn_mode_of_action, disease_id, group_name  from products where group_name like ? limit ?,?;",
            ("%" + group_name + "%", offset, limit),
            )

            list = cursor.fetchall()

            columns = [column[0] for column in cursor.description]
            results = []
            for row in list:
                results.append(dict(zip(columns, row)))
            
            list = results


            if not list:
                message = "Simlar Product not found"
                message_bn = "অনুরূপ পণ্য পাওয়া যায় নি"
                code = "4000"
                status = "error"

            else:
                message = "Similar Product found"
                message_bn = "অনুরূপ পণ্য পাওয়া গেছে"
                code = "2000"
                status = "success"

        return jsonify(
            message=message,
            message_bn=message_bn,
            code=code,
            status=status,
            data=list,
        )

class DiseaseDetails(Resource):
    def post(self):
        parser_s = reqparse.RequestParser()
        parser_s.add_argument("api_key", type=str)
        parser_s.add_argument("disease_id", type=str)
        parser_s.add_argument("lat", type=str)
        parser_s.add_argument("lon", type=str)

        args = parser_s.parse_args()

        disease_id = args["disease_id"]
        api_key = args["api_key"]
        lat = args["lat"]
        lon = args["lon"]
        data = {}

        if api_key != API_KEY_GLOBAL:
            message = "Api key not matched"
            code = "4000"
            status = "error"
            message_bn = "এপি আই কী মিলছে না"

        elif disease_id is None:
            message = "Disease Id required"
            message_bn = "রোগের আইডি প্রয়োজন"
            code = "$000"
            status = "error"

        else: 
            message = "Disease Details found"
            message_bn = "রোগের বিবরণ পাওয়া গেছে"
            code = "2000"
            status = "success"

            top_five_nearest_dealers = []

            if lat is not None and lon is not None:
                top_five_nearest_dealers = get_top_five_nearest_dealers(lat, lon)

            recommended_solutions = get_recommended_solutions(disease_id)

            data = {
                "recommended_solutions": recommended_solutions,
                "nearest_dealers": top_five_nearest_dealers,
            }

        return jsonify(
            message=message, message_bn=message_bn, code=code, status=status, data=data
        )

class DiseaseSearchHistories(Resource):
    def post(self):
        parser_s = reqparse.RequestParser()
        parser_s.add_argument("offset", type=int)
        parser_s.add_argument("limit", type=int)
        parser_s.add_argument("api_key", type=str)
        parser_s.add_argument("disease_name", type=str)
        parser_s.add_argument("user_id", type=int)

        args = parser_s.parse_args()

        disease_name = args["disease_name"]
        offset = args["offset"]
        limit = args["limit"]
        api_key = args["api_key"]
        user_id = args["user_id"]
        list = []

        if api_key != API_KEY_GLOBAL:
            message = "Api key not matched"
            code = "4000"
            status = "error"
            message_bn = "এপি আই কী মিলছে না"
            
        elif offset is None or limit is None or user_id is None:
            message = "Offset, Limit and User Id are required"
            message_bn = "অফসেট, সীমাবদ্ধতা এবং ব্যবহারকারীর আইডি প্রয়োজনীয়"
            code = "2000"
            status = "error"

        else:
            connection = sqlite3.connect(DB_PATH)
            cursor=connection.cursor()
            if disease_name is None:
                cursor.execute(
                    "select ifnull(id,'') as id , ifnull(image,'') as image, ifnull(accuracy,'') as accuracy, ifnull(name,'') as en_name, ifnull(details,'') as en_details, ifnull(bn_name,'') as bn_name, ifnull(bn_details,'') as bn_details,disease_id,created_time as date_time, ifnull(detection_type,'') as detection_type, ifnull(lat,'') as lat, ifnull(lon,'') as lon from disease_histories where user_id = ? order by id desc limit ?,?;",
                    (user_id, offset, limit),
                )
            else:
                cursor.execute(
                    "select ifnull(id,'') as id , ifnull(image,'') as image, ifnull(accuracy,'') as accuracy, ifnull(name,'') as en_name, ifnull(details,'') as en_details, ifnull(bn_name,'') as bn_name, ifnull(bn_details,'') as bn_details,disease_id,created_time as date_time, ifnull(detection_type,'') as detection_type, ifnull(lat,'') as lat, ifnull(lon,'') as lon from disease_histories where user_id =? AND (name like ? OR bn_name like ?) order by id desc limit ?,? ;",
                    (
                        user_id,
                        "%" + disease_name + "%",
                        "%" + disease_name + "%",
                        offset,
                        limit,
                    ),
                )

            list = cursor.fetchall()

            columns = [column[0] for column in cursor.description]
            results = []
            for row in list:
                results.append(dict(zip(columns, row)))
            
            list = results


            if not list:
                message = "Disease search history not found."
                message_bn = "রোগ অনুসন্ধানের ইতিহাস পাওয়া যায় নি।"
                code = "4000"
                status = "error"
            else:
                message = "Disease search history found."
                message_bn = "রোগ অনুসন্ধানের ইতিহাস পাওয়া গেছে"
                code = "2000"
                status = "success"

        return jsonify(
            message=message,
            message_bn=message_bn,
            code=code,
            status=status,
            data=list,
        )

class VerifyOtp(Resource):
    def post(self):
        parser_s = reqparse.RequestParser()
        parser_s.add_argument("api_key", type=str)
        parser_s.add_argument("otp", type=str)
        parser_s.add_argument("phone_number", type=str)
        parser_s.add_argument("android_id", type=str)
        parser_s.add_argument("device_name", type=str)
        parser_s.add_argument("os_version", type=str)
        parser_s.add_argument("sdk_version", type=str)
        parser_s.add_argument("version_code", type=str)
        parser_s.add_argument("version_name", type=str)
        args = parser_s.parse_args()
        api_key = args["api_key"]
        otp = args["otp"]
        phone_number = args["phone_number"]
        android_id = args["android_id"]
        device_name = args["device_name"]
        os_version = args["os_version"]
        sdk_version = args["sdk_version"]
        version_code = args["version_code"]
        version_name = args["version_name"]
        message=None
        message_bn=None
        code=None
        status=None
        user_id=None
        data = {}
        
        if api_key is None or phone_number is None or not android_id:
            message = "Api Key, Phone Number, Android Id are required"
            message_bn = "এপি কী, ফোন নম্বর, অ্যান্ড্রয়েড আইডি প্রয়োজন"
            code = "4000"
            status = "error"
        elif api_key != API_KEY_GLOBAL:
            message = "Api key not matched"
            message_bn = "এপি কী মিলছে না"
            code = "4000"
            status = "error"
        else:
            last_otp = 0
            last_otp_time = ""
            
            if len(phone_number) == 11:
                phone_number = "+88" + phone_number
            
            connection = sqlite3.connect(DB_PATH)
            cursor=connection.cursor()
            cursor.execute(
                "SELECT last_otp, last_otp_time,otp_count,user_id,status FROM devices WHERE phone_number=? and android_id=?", (phone_number,android_id)
            )
            
            row = cursor.fetchone()
            cursor.close()
            connection.commit()
            connection.close()
    
            if row:
                last_otp = row[0]
                last_otp_time = row[1]
                otp_count = row[2]
                user_id = row[3] # this could be null
                status = row[4]
                otp_time_diff = 0
                d1 = datetime.strptime(datetime.now().strftime("%m/%d/%Y %H:%M:%S"),"%m/%d/%Y %H:%M:%S")
                d2 = datetime.strptime(last_otp_time,"%m/%d/%Y %H:%M:%S")
                otp_time_diff = abs((d2 - d1).days)
                
                if  int(otp_time_diff) > 1:
                    status = "otp_time_over"
                    update_device(android_id, phone_number,  status, "", otp_count)
                    message = "OTP Time Over"
                    message_bn = "ওটিপি সময় শেষ"
                    code = "2000"
                    
                elif otp != last_otp:
                    message = "OTP not matched"
                    message_bn = "ওটিপি মিলছে না"
                    code = "4000"
                    update_device(android_id,phone_number,status,last_otp,otp_count,user_id,device_name,os_version,sdk_version,version_code,version_name)
                    status = "otp_not_matched"
            
                else:
                    message = "Otp Matched"
                    message_bn = "ওটিপি মিলে গেছে"
                    code = "2000"
                    
                    if status == 'otp_sent_new_user_existing_device' or status == 'otp_sent_new_user_new_device':
                        user_id = insert_user(phone_number)
                        status = "otp_matched" 
                        update_device(android_id,phone_number,status,last_otp,otp_count,user_id,device_name,os_version,sdk_version,version_code,version_name)
                    
        data = {"user_id": user_id, "phone_number": phone_number}
        return jsonify(
            message = message,
            message_bn = message_bn,
            code = code,
            status = status,
            data = data
            )

def send_otp(phone_number):
    digits = "0123456789"
    otp = ""
    for i in range (6):
        otp += digits[math.floor(random.random()*10)]
    return otp
    
def update_device(android_id,phone_number,status=None,otp=None,otp_count=None,user_id=None,device_name=None,os_version=None,sdk_version=None,version_code=None,version_name=None ):
    current_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    connection = sqlite3.connect(DB_PATH)
    cursor=connection.cursor()
    cursor.execute(
        "UPDATE devices SET android_id = ?, device_name=?,os_version=?,sdk_version=?,version_code=?,version_name=?, updated_time=?,status=?,user_id=?,phone_number=?,last_otp=?,last_otp_time=?,otp_count=? WHERE android_id=? and phone_number=?",
        (android_id, device_name, os_version, sdk_version, version_code, version_name, current_time, status, user_id, phone_number, otp, current_time, otp_count, android_id,phone_number
        ),
        )
        
    cursor.close()
    connection.commit()
    connection.close()
    
def insert_device(android_id,phone_number,status=None, otp=None, otp_count=None, user_id=None):
    current_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    print("insert device")
    connection = sqlite3.connect(DB_PATH)
    cursor=connection.cursor()
    cursor.execute(
    "INSERT INTO devices(user_id,android_id,phone_number,last_otp,status,created_time,last_otp_time,otp_count) VALUES(?,?,?,?,?,?,?,?)",
    (user_id,android_id,phone_number,otp,status,current_time,current_time,0),
    )
    device_id=cursor.lastrowid
    # cursor.close()
    connection.commit()
    connection.close()
    return device_id
    
def insert_user(phone_number):
    current_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    connection = sqlite3.connect(DB_PATH)
    cursor=connection.cursor()

    result = cursor.execute(
        "INSERT INTO users(phone_no,created_time) VALUES(?,?)",(phone_number,current_time,),
    )
    user_id = result.lastrowid
    cursor.close()
    connection.commit()
    connection.close()
        
    return user_id

class UserRegistration(Resource):
    def post(self):
        parser_s = reqparse.RequestParser()
        parser_s.add_argument("api_key", type=str)
        parser_s.add_argument("phone_number", type=str)
        parser_s.add_argument("api_token", type=str)
        parser_s.add_argument("android_id", type=str)
        parser_s.add_argument("lat", type=str)
        parser_s.add_argument("lon", type=str)
        args = parser_s.parse_args()
        api_key = args["api_key"]
        phone_number = args["phone_number"]
        android_id = args["android_id"]

        data = {}


        if api_key != API_KEY_GLOBAL or api_key is None or phone_number is None or not android_id:
            message = "Api Key, Phone Number, Device Id are required"
            message_bn = "ব্যবহারকারীর ফোন নম্বর এবং এপিআই আইডি প্রয়োজন"
            code = "4000"
            status = "error"

        elif api_key != API_KEY_GLOBAL:
            message = "Api key not matched"
            message_bn = "এপিআই কী মিলছে না"
            code = "2000"
            status = "error"

        else:
            my_number = phonenumbers.parse(phone_number, "BD")
            is_valid_phone_number = phonenumbers.is_valid_number(my_number)

            if not is_valid_phone_number:
                message = "Phone Number Invalid"
                message_bn = "ফোন নম্বর অবৈধ"
                code = "4000"
                status = "error"
            
            else:
                if len(phone_number) == 11:
                    phone_number = "+88" + phone_number
            
                connection=sqlite3.connect(DB_PATH)
                cursor=connection.cursor()
                cursor.execute(
                    "SELECT id,phone_no FROM users where phone_no=?",(phone_number,)
                )
                
                row = cursor.fetchone()
                cursor.close()
                connection.commit()
                connection.close()
                user_existing_id = None
                message_bn = None
                code = None
                status = None
                data = {}

                if row is not None:
                    user_existing_id = row[0]
                connection=sqlite3.connect(DB_PATH)
                cursor=connection.cursor()

                cursor.execute(
                    "SELECT user_id,android_id,status,otp_count,last_otp_time FROM devices where phone_number=? and android_id=?",(phone_number,android_id,),
                )
                row = cursor.fetchone()
                cursor.close()
                connection.commit()
                connection.close()
                user_existing_android_id = None
                otp_count=0
                print('status before if else --- >', status)
                if row is not None:
                    user_existing_android_id = row[1]
                    user_existing_status = row[2]
                    otp_count = row[3]
                    
                message = ""
                
                if otp_count>=3:
                    status = "otp_maximum_limit_exceeded"
                    update_device(android_id, phone_number,  status, None, otp_count)
                    message = "Maximum Limit Exceeded"
                    message_bn = "Maximum Limit Exceeded"
                    code = "2000"
                    data = {"user_id": "", "phone_number": phone_number}
                    
                
                elif user_existing_id is not None and android_id == user_existing_android_id and user_existing_status == 'otp_matched':
                    message = "User login successfully"
                    status = "success"
                    message_bn = "বব্যবহারকারীর লগইন সফল"
                    code = 2000
                    
                elif user_existing_id is not None and android_id == user_existing_android_id and status!= 'otp_matched':
                    otp = send_otp(phone_number)
                    status = "otp_sent_existing_user_existing_device"

                    update_device(android_id, phone_number,  status, otp, otp_count+1)
                    
                    message = "Otp Sent"
                    message_bn = "Otp Sent"
                    code = "2000"

                elif user_existing_id is not None and android_id != user_existing_android_id and status!= 'otp_matched':
                    otp = send_otp(phone_number)
                    status = "otp_sent_existing_user_new_device"

                    print(status)

                    insert_device(android_id, phone_number,  status, otp, otp_count+1, user_id=user_existing_id)
                    
                    message = "Otp Sent"
                    message_bn = "Otp Sent"
                    code = "2000"
                    
                elif user_existing_id is None and android_id == user_existing_android_id and status!= 'otp_matched':
                    print("user_existing_id is None and android_id == user_existing_android_id and status!= 'otp_matched'")
                    otp = send_otp(phone_number)
                    status = "otp_sent_new_user_existing_device"
                    update_device(android_id, phone_number, status, otp, otp_count+1)
                    message = "OTP Sent"
                    message_bn = "OTP Sent"
                    code = "2000"

                elif user_existing_id is None and android_id != user_existing_android_id and status!= 'otp_matched':
                    otp = send_otp(phone_number)
                    status = "otp_sent_new_user_new_device"
                    print('USER existing ID ---->', user_existing_id, '<----- Here It is')
                    print("Here",status)
                    print(android_id,'-----', user_existing_android_id)
                    print(type(android_id),'-----', type(user_existing_android_id))
                    insert_device(android_id, phone_number, status, otp, 0)
                    message = "OTP Sent"
                    message_bn = "OTP Sent"
                    code = "2000"
                data = {"user_id": user_existing_id, "phone_number": phone_number}

        return jsonify(
            message=message, message_bn=message_bn, code=code, status=status,
            data=data
        )               

        

class Users(Resource):
    def post(self):
        connection=sqlite3.connect(DB_PATH)
        cursor=connection.cursor()
        cursor.execute("select * from users;")
        
        list = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        results = []
        for row in list:
            results.append(dict(zip(columns, row)))
        
        list = results

        try:
            message = "Users found."
            message_bn = "ব্যবহারকারী খুঁজে পাওয়া গেছে"
            code = "2000"
            status = "success"
        except Exception as e:
            message = "Invalid."
            code = "404"
            status = "error"
            message_bn = "অবৈধ"
        return jsonify(
            message=message,
            message_bn=message_bn,
            code=code,
            status=status,
            data=list,
        )

class Devices(Resource):
    def post(self):
        connection=sqlite3.connect(DB_PATH)
        cursor=connection.cursor()
        cursor.execute("select * from devices;")
        
        list = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        results = []
        for row in list:
            results.append(dict(zip(columns, row)))
        
        list = results

        try:
            message = "Devices found."
            message_bn = "ডিভাইস পাওয়া গেছে"
            code = "1000"
            status = "success"
        except Exception as e:
            message = "Invalid."
            code = "404"
            status = "error"
            message_bn = "অবৈধ"
        return jsonify(message=message, message_bn=message_bn, code=code, status=status, data=list)

def sampling(selection, offset=0, limit=None):
    return selection[offset:(limit + offset if limit is not None else None)]

class Dealers(Resource):
    def post(self):
        parser_s = reqparse.RequestParser()

        parser_s.add_argument("offset", type=int)
        parser_s.add_argument("limit", type=int)
        parser_s.add_argument("name", type=str)
        parser_s.add_argument("api_key", type=str)
        parser_s.add_argument("address", type=str)
        parser_s.add_argument("lat", type=str)
        parser_s.add_argument("lon", type=str)

        args = parser_s.parse_args()

        offset = args["offset"]
        limit = args["limit"]
        name = args["name"]
        api_key = args["api_key"]
        address = args["address"]
        lat = args["lat"]
        lon = args["lon"]

        result = []

        if api_key != API_KEY_GLOBAL:
            message = "Api key not matched"
            code = "4000"
            status = "error"
            message_bn = "এপি আই কী মিলছে না"

        elif offset is None or limit is None:
            message = "Offset and Limit are required"
            message_bn = "অফসেট এবং সীমাবদ্ধতা প্রয়োজন"
            code = "4000"
            status = "error"

        else:
            
            connection=sqlite3.connect(DB_PATH)
            cursor=connection.cursor()
            

            if name is not None and address is not None:
                cursor.execute(
                    "select ifnull(id, '') as id, ifnull(name,'') as shop_name, ifnull(contact_name,'') as contact_name,ifnull(address,'') as shop_address, ifnull(mobile,'') as mobile, 'https://api.drchashi.com/static/dealer_images/' || ifnull(image,'default.png') as image,  ifnull(lat,0.0) as lat,  ifnull(lon,0.0) as lon from dealers where (name like ? OR address like ? OR contact_name like ?) and address like ?limit ?,?;",
                    (
                        "%" + name + "%",
                        "%" + name + "%",
                        "%" + name + "%",
                        "%" + address + "%",
                        offset,
                        limit,
                    ),
                )

            elif address is not None:
                cursor.execute(
                    "select ifnull(id, '') as id, ifnull(name,'') as shop_name, ifnull(contact_name,'') as contact_name,ifnull(address,'') as shop_address, ifnull(mobile,'') as mobile, 'https://api.drchashi.com/static/dealer_images/' || ifnull(image,'default.png') as image,  ifnull(lat,0.0) as lat,  ifnull(lon,0.0) as lon from dealers where address like ?;",
                    ("%" + address + "%"),
                )

            elif name is not None:
                cursor.execute(
                    "select ifnull(id, '') as id, ifnull(name,'') as shop_name, ifnull(contact_name,'') as contact_name,ifnull(address,'') as shop_address, ifnull(mobile,'') as mobile, 'https://api.drchashi.com/static/dealer_images/' || ifnull(image,'default.png') as image,  ifnull(lat,0.0) as lat,  ifnull(lon,0.0) as lon from dealers where name like ? OR address like ? OR contact_name like ?;",
                    ("%" + name + "%", "%" + name + "%", "%" + name + "%"),
                )

            else:
                cursor.execute(
                    "select ifnull(id, '') as id, ifnull(name,'') as shop_name, ifnull(contact_name,'') as contact_name,ifnull(address,'') as shop_address, ifnull(mobile,'') as mobile, 'https://api.drchashi.com/static/dealer_images/' || ifnull(image,'default.png') as image,  ifnull(lat,0.0) as lat,  ifnull(lon,0.0) as lon from dealers;",
                )
            

            latlons = cursor.fetchall()

            columns = [column[0] for column in cursor.description]
            results = []
            for row in latlons:
                results.append(dict(zip(columns, row)))

            for x in results:
                x['distance'] = distance_between_two_lat_lon(float(x["lat"]), float(x["lon"]), float(lat), float(lon))

            nearest_dealers = sorted(
                results,
                key=lambda d: 
                    d["distance"]
            )

            result = sampling(nearest_dealers, offset=offset, limit=limit)
        
            for x in result:
                x['distance_en'] = str(x['distance']) + " Kilometre"
                x['distance_bn'] = str(x['distance']) + " কিলোমিটার"

            if not result:
                message = "Dealer Information not found"
                message_bn = "ডিলার তথ্য পাওয়া যায়নি"
                code = "4000"
                status = "error"

            else:
                message = "Dealer information found"
                message_bn = "ডিলারতথ্য পাওয়া গেছে"
                code = "2000"
                status = "success"

        return jsonify(
            message=message,
            message_bn=message_bn,
            code=code,
            status=status,
            data=result,
        ) 


# def find_nearest_lat_lon(lon1, lat1, lon2, lat2):
#    R = 6371000 #radius of the Earth in
#    x = (lon2 - lon1) * cos(0.5*(lat2+lat1))
#    y = (lat2 - lat1)
#    return (2*pi*R/360) * sqrt( x*x + y*y )


def distance_between_two_lat_lon(lat1, lon1, lat2, lon2):
    '''Provides the distance between two lat lon position'''
    R = 6373.0
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
 

    """ coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)

    distance = geopy.distance.geodesic(coords_1, coords_2).km """

    return round(distance, 2)
        

def get_recommended_solutions(disease_id):
    '''Provides recommended solution for the detected disease'''
    recommended_solutions = []
    connection=sqlite3.connect(DB_PATH)
    cursor=connection.cursor()
    query = cursor.execute(
        "select ifnull(id,'') as id , ifnull(crop_id,'') as crop_id, 'https://api.drchashi.com/static/product_images/' || ifnull(image_name,'default.png') as image, ifnull(en_name,'') as en_name, ifnull(en_group,'') as en_group,ifnull(en_amount,'400 ml') as en_amount, ifnull(en_details,'') as en_deails, ifnull(en_active_ingredients,'') as en_active_ingredients, ifnull(en_mode_of_action,'') as en_mode_of_action, ifnull(bn_name,'') as bn_name, ifnull(bn_group,'') as bn_group, ifnull(bn_amount,'400 মিলি') as bn_amount, ifnull(bn_details,'') as bn_details, ifnull(bn_active_ingredients,'') as bn_active_ingredients, ifnull(bn_mode_of_action,'') as bn_mode_of_action, disease_id, group_name from products where (',' || disease_id || ',') LIKE '%,"
        + str(disease_id)
        + ",%'"
    )
    recommended_solutions = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    results = []
    for row in recommended_solutions:
        results.append(dict(zip(columns, row)))

    return results


def get_top_five_nearest_dealers(lat, lon):
    ''' Prvides top 5 nearest dealers'''
    connection=sqlite3.connect(DB_PATH)
    cursor=connection.cursor()
    cursor.execute(
        "select ifnull(id, '') as id, ifnull(name,'') as shop_name, ifnull(contact_name,'') as contact_name,ifnull(address,'') as shop_address, ifnull(mobile,'') as mobile, 'https://api.drchashi.com/static/dealer_images/' || ifnull(image,'default.png') as image, ifnull(lat,0.0) as lat,  ifnull(lon,0.0) as lon from dealers"
    )

    latlons = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    results = []
    for row in latlons:
        results.append(dict(zip(columns, row)))

    latlons = results

    for x in latlons:
        x['distance'] = distance_between_two_lat_lon(float(x["lat"]), float(x["lon"]), float(lat), float(lon))

    nearest_dealers = sorted(
        latlons,
        key=lambda d: 
            d["distance"]
    )

    for x in nearest_dealers:
        x['distance_en'] = str(x['distance'])+" Kilometre"
        x['distance_bn'] = str(x['distance'])+" কিলোমিটার"
 
    top_five_nearest_dealers =  sampling(nearest_dealers,offset=0,limit=4)

    # print(top_five_nearest_dealers)

    return top_five_nearest_dealers

api.add_resource(Users, "/getUsers")
api.add_resource(Devices, "/getDevices")
api.add_resource(UserRegistration, "/setUserRegistration")
api.add_resource(Products, "/getProducts")
api.add_resource(Crops, "/getCrops")
api.add_resource(SearchGuides, "/getSearchGuides")
api.add_resource(Customers, "/getCustomers")
api.add_resource(SimilarProducts, "/getSimilarProducts")
api.add_resource(DiseaseSearchHistories, "/getDiseaseSearchHistories")
api.add_resource(DiseaseDetails, "/getDiseaseDetails")
api.add_resource(DiseaseDetectionInformation, "/getDiseaseDetectionInformation")
api.add_resource(Dealers, "/getDealers")
api.add_resource(VerifyOtp, "/verifyOtp")

connection.set_trace_callback(print)
connection.commit()
connection.close()
# this one is to run the code on aws server
# if __name__ == '__main__':
#     app.run(host = '0.0.0.0', port = '443', ssl_context = ('/etc/letsencrypt/live/api.drchashi.com/fullchain.pem', '/etc/letsencrypt/live/api.drchashi.com/privkey.pem'))

# this one is to run the code on local machine
if __name__ == "__main__":
    app.run(host="127.0.0.1", port="5002", debug=True)


