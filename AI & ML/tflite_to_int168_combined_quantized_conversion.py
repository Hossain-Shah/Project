import tensorflow as tf
import numpy as np
images = 'E:/Official purpose/Sprint - 31/Final_Mango_Dataset'


def representative_dataset():
  for data in tf.data.Dataset.from_tensor_slices((images)).batch(32).take(100):
    yield [tf.dtypes.cast(data, tf.float32)]


def representative_dataset():
    for _ in range(100):
      data = np.random.rand(1, 224, 224, 3)
      yield [data.astype(np.float32)]


tflite_model = tf.keras.models.load_model('E:/Official purpose/Sprint - 6/Finalized_model/Final_Mango_In80.h5')
converter = tf.lite.TFLiteConverter.from_keras_model(tflite_model)
converter.representative_dataset = representative_dataset
converter.optimizations = [tf.lite.Optimize.DEFAULT]
#converter.representative_dataset = representative_dataset
#converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
#converter.inference_input_type = tf.int8  # or tf.uint8
#converter.inference_output_type = tf.int8  # or tf.uint8
#converter.target_spec.supported_types = [tf.float16]
converter.target_spec.supported_ops = [tf.lite.OpsSet.EXPERIMENTAL_TFLITE_BUILTINS_ACTIVATIONS_INT16_WEIGHTS_INT8]
#converter.target_spec.supported_ops = [tf.lite.OpsSet.EXPERIMENTAL_TFLITE_BUILTINS_ACTIVATIONS_INT16_WEIGHTS_INT8, tf.lite.OpsSet.TFLITE_BUILTINS]
tflite_quant_model = converter.convert()
open("E:/Official purpose/Sprint - 6/Final_Mango_In80_int168_combined_quantized.tflite" , "wb").write(tflite_quant_model)
