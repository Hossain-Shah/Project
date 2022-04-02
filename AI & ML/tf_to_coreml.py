import tensorflow as tf
import coremltools as ct
model = tf.keras.models.load_model('E:/PureStrength_COCOcandidate_task.h5')
ios_converted_model = ct.convert(model)
ios_converted_model.save('E:/PureStrength_COCOcandidate_task.mlmodel')
