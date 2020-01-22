import numpy as np
from sklearn import preprocessing
test_labels = ['green','red','black']
encoder = preprocessing.LabelEncoder()
encoder.fit(test_labels)
encoded_values = encoder.transform(test_labels)
print("\nLabels =", test_labels)
print("Encoded values =", list(encoded_values))
decoded_list = encoder.inverse_transform(encoded_values)
print("\nDecoded labels =", list(decoded_list))
