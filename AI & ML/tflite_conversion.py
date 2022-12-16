import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow import lite
tflite_model = tf.keras.models.load_model('rice_augmented_annotated_segmented_bkgroundremoved_model_inception_299.h5')
converter = tf.lite.TFLiteConverter.from_keras_model(tflite_model)
tfmodel = converter.convert()
open("rice_augmented_annotated_segmented_bkgroundremoved_model_inception_299.tflite", "wb") .write(tfmodel)
