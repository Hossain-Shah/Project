import os
import numpy as np
import pandas as pd
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from sklearn import tree, metrics
import graphviz
data =pd.read_csv('C:/Users/HP/Desktop/task/csv_result-car.csv',names=['buying','maint','doors','persons','lug_boot','safety','class'])
print(data.head())
print(data.info())
data['class'],class_names = pd.factorize(data['class'])
print(class_names)
print(data['class'].unique())
data['buying'],_ = pd.factorize(data['buying'])
data['maint'],_ = pd.factorize(data['maint'])
data['doors'],_ = pd.factorize(data['doors'])
data['persons'],_ = pd.factorize(data['persons'])
data['lug_boot'],_ = pd.factorize(data['lug_boot'])
data['safety'],_ = pd.factorize(data['safety'])
print(data.head())
print(data.info())

