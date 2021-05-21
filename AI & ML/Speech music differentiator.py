import numpy as np
import os
import pickle
import random
import pandas as pd
import sklearn
import scipy.io.wavfile as wav
from os import path
from pydub import AudioSegment
from python_speech_features import mfcc
from sklearn.metrics import classification_report
from collections import defaultdict
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
directory = "D:/Pycharm/Program/AI_Stat_ANN/music_speech"
filelist = []
for path, subdirs, files in os.walk(directory):
    for file in files:
        if (file.endswith('.wav') or file.endswith('.WAV')):
            filelist.append(os.path.join(path, file))
number_of_files = len(filelist)
print(number_of_files)


def feature_extraction(file):
  features = []
  (sampleRate, data) = wav.read(file)
  mfcc_feature = mfcc(data, sampleRate, winlen=0.020, appendEnergy=False)
  meanMatrix = mfcc_feature.mean(0)
  for x in meanMatrix:
    features.append(x)
  return features


datasetDirectory = "D:/Pycharm/Program/AI_Stat_ANN/music_speech/"
featureSet = []
i = 0
for folder in os.listdir(datasetDirectory):
    i += 1
    if i > 9: # the number of genre is 9
        break
    for files in os.listdir(datasetDirectory+folder):
      x = datasetDirectory+folder+"/"+files
      features = feature_extraction(x)
      j = 0
      for x in features:
        featureSet.append(x)
        j = j+1
        if(j%13 == 0): # the number of feaatures is 13
          featureSet.append(i)


for i in range(14, 28):
  print (featureSet[i])
df = pd.DataFrame(columns=['m1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'm10', 'm11', 'm12', 'm13', 'target'])
i = 1
n = []
for j in featureSet:
  n.append(j)
  #13 features + 1 taget
  if(i%14 == 0):
    df = df.append({'m1':n[0],'m2':n[1],'m3':n[2],'m4':n[3],'m5':n[4],'m6':n[5],'m7':n[6],'m8':n[7],'m9':n[8],'m10':n[9],'m11':n[10],'m12':n[11],'m13':n[12],'target':n[13]}, ignore_index=True)
    n=[]
  i = i+1
print(df)
x1 = df[['m1','m2','m3','m4','m5','m6','m7','m8','m9','m10','m11','m12','m13']]
print(x1.shape)
Y = df[['target']]
print(Y.shape)
X_train, X_test, y_train, y_test = train_test_split(x1, Y, test_size=0.2, random_state=42)
clf = LogisticRegression(random_state=0).fit(X_train, y_train)
predicted_value = clf.predict(X_test)
print(predicted_value)
#sklearn.metrics.plot_confusion_matrix(clf, X_test, y_test)
print(classification_report(y_test, predicted_value))
#Extract the feature from the audio_file
audio_file = "file_example_WAV_5MG.wav"
audio_feature = feature_extraction(audio_file)
results = defaultdict(int)
i = 1
for folder in os.listdir("D:/Pycharm/Program/AI_Stat_ANN/music_speech/"):
    results[i] = folder
    i += 1
pred_audio = clf.predict([audio_feature])
print(results[int(pred_audio)])

