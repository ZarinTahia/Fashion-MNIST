# -*- coding: utf-8 -*-
"""Fashion MNIST.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MzLpgWNzJdm_oJNkZFR0I_3Jq8yv4vxG
"""

!pip install sklearn

import matplotlib.pyplot as plt
import sklearn as sk
import pandas as pd
import numpy as np
from sklearn.metrics import balanced_accuracy_score,roc_auc_score,make_scorer
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, classification_report
import seaborn as sns

import tensorflow as tf
import sklearn
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Sequential

fashion_MNIST_train = pd.read_csv("/content/drive/MyDrive/Fashion MNIST-Data/fashion-mnist_train.csv")
fashion_MNIST_test = pd.read_csv("/content/drive/MyDrive/Fashion MNIST-Data/fashion-mnist_test.csv")

fashion_MNIST_train.head()

fashion_MNIST_test.head()

print(fashion_MNIST_train.shape)
print(fashion_MNIST_test.shape)

fashion_MNIST_train.keys()

fashion_MNIST_train.info()

fashion_MNIST_test.info()

"""Visualize with 2*5 grid"""

classes = {0:'tshirt',1:'trouser',2:'pullover',3:'dress',4:'coat',5:'sandal',6:'shirt',7:'sneaker',8:'bag',9:'ankle boot'}

fig, axes = plt.subplots(3, 4, figsize = (10,8))

pixel_values = fashion_MNIST_train.drop('label', axis=1).values
title = fashion_MNIST_train.iloc[:, 0].values

for i, ax in enumerate(axes.flat):

  image = pixel_values[i].reshape(28, 28)
  ax.imshow(image, cmap='gray')
  ax.set_title(classes[title[i]])
  ax.axis('off')

plt.tight_layout()
plt.show()

fig, axes = plt.subplots(3, 4, figsize = (10,8))

pixel_values = fashion_MNIST_test.drop('label', axis=1).values
title = fashion_MNIST_test.iloc[:, 0].values

for i, ax in enumerate(axes.flat):

  image = pixel_values[i].reshape(28, 28)
  ax.imshow(image)
  ax.set_title(classes[title[i]])
  ax.axis('off')

plt.tight_layout()
plt.show()

fashion_MNIST_train.isnull().sum()

fashion_MNIST_test.isnull().sum()

labelCount = fashion_MNIST_train['label'].value_counts()
print(labelCount)

labelCount = fashion_MNIST_test['label'].value_counts()
print(labelCount)

x_train = fashion_MNIST_train.drop(['label'],axis=1)
y_train = fashion_MNIST_train['label'].copy()
x_test = fashion_MNIST_test.drop(['label'],axis=1)
y_test = fashion_MNIST_test['label'].copy()

x_train

y_train

x_train.describe()

x_test.describe()

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
x_train = pd.DataFrame(scaler.fit_transform(x_train), columns=x_train.columns)
x_test = pd.DataFrame(scaler.fit_transform(x_test), columns=x_test.columns)

x_train.describe()

x_test.describe()

def get_model():
  model = Sequential()
  model.add(Flatten(input_shape=(784,)))
  model.add(Dense(64, activation='relu'))
  model.add(Dense(128, activation='relu'))
  model.add(Dense(10, activation= 'softmax'))
  return model

model = get_model()

model.summary()

model.layers

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy',metrics=['accuracy'])
model.fit(x_train,y_train, epochs=50)
model.evaluate(x_test, y_test)

pred = model.predict(x_test)
print(pred)

model.evaluate(x_test,y_test)

pred = np.argmax(pred, axis = 1)

accuracy = accuracy_score(y_test, pred)*100
print("Accuracy Soure",accuracy)

result = classification_report(y_test,pred)
print(result)

pd.crosstab(y_test,pred)
conf_matrix = confusion_matrix(y_test, pred)

classlabel = ['tshirt','trouser','pullover','dress','coat','sandal','shirt','sneaker','bag','ankle boot']

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='YlGnBu',
            xticklabels= classlabel, yticklabels= classlabel)
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title(f'Confusion Matrix\nAccuracy: {accuracy:.2f}')
plt.show()