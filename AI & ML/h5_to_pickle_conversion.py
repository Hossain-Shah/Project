from keras.models import load_model
import pickle
import sys
sys.setrecursionlimit(5000)
model = load_model('E:/Official purpose/Sprint - 2/mango_model_justification_inception.h5')
pickle.dump(model, open('mango_model_justification_inception.pkl', 'wb'))
