# get all the packeges ready

import os
import numpy as np
import random as ran
import tensorflow as tf
import keras
from keras import backend as K
K.tensorflow_backend._get_available_gpus()
from __future__ import print_function
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, Conv3D,MaxPooling3D
from keras.layers.normalization import BatchNormalization
from keras import initializers
from keras.callbacks import ModelCheckpoint, TensorBoard, CSVLogger
from keras.optimizers import Adam, Adadelta
from keras_alexnet_dataloaders import *
# load data
# this process depends the data, here loading numpy arrays only
x_train = np.load('/data/x_train.npy')
y_train = np.load('/data/y_train.npy')
x_val = np.load('/data/x_val.npy')
y_val = np.load('/data/y_val.npy')
x_test = np.load('/data/x_test.npy')
y_test = np.load('/data/y_test.npy')

import numpy as np
n_train = x_train.shape[0]

## This indicates the size of X_val
n_valid = x_val.shape[0]

## This is size of X_test
n_test = x_test.shape[0]

## Question has its own answer, just put the shape in the end :D
image_shape = x_train[0].shape

## Glad numpy has np.unique, y_train is the tuple of labels,
#unique members of this tuple it gives number of classes
n_classes = np.unique(y_val).size

print("Number of training examples =", n_train)
print ("Number of validation examples", n_valid)
print ("Number of test examples", n_test)
print("Image data shape =", image_shape)
print("Number of classes =", n_classes)

from sklearn.utils import shuffle
x_train, y_train = shuffle(x_train, y_train)
x_val, y_val = shuffle(x_val, y_val)
x_test, y_test = shuffle(x_test, y_test)

BATCH_SIZE = 8
NUM_CLASSES = n_classes
NUM_EPOCHS = 50
save_dir = os.path.join(os.getcwd(), 'saved_models')
model_name = 'keras_alexnet_trained_model.h5'


print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_val.shape[0], 'valid samples')
print(x_test.shape[0], 'test samples')


y_train = keras.utils.to_categorical(y_train, NUM_CLASSES)
y_val = keras.utils.to_categorical(y_val, NUM_CLASSES)
y_test = keras.utils.to_categorical(y_test, NUM_CLASSES)

#Importing keras functions to build the convnet
from __future__ import print_function
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D,MaxPooling2D,AveragePooling2D, Input, ZeroPadding2D
from keras.layers.normalization import BatchNormalization
from keras import initializers
from keras.callbacks import ModelCheckpoint, TensorBoard, CSVLogger,EarlyStopping,ReduceLROnPlateau
from keras.optimizers import Adam, Adadelta,RMSprop, Adamax, Nadam, SGD
import os



#define batch size
BATCH_SIZE = 32
# Design model
model = Sequential()
 # Architecture
model.add(Conv2D(filters=96,kernel_size=(3,3),activation='relu',strides=1,padding='same',kernel_initializer='glorot_uniform',input_shape=image_shape))
model.add(MaxPooling2D((2,2),strides=(2,2)))
model.add(Conv2D(filters=256, kernel_size=(3,3), activation='relu', strides=(2,2,2), padding='same'))
model.add(MaxPooling2D((2,2),strides=(2,2)))
model.add(Conv2D(filters=384, kernel_size=(3,3), activation='relu', strides=(2,2,2), padding='same'))
model.add(Conv2D(filters=384, kernel_size=(3,3), activation='relu', strides=(2,2,2), padding='same'))
model.add(Conv2D(filters=256, kernel_size=(3,3), activation='relu', strides=(2,2,2), padding='same'))
model.add(MaxPooling2D((2,2),strides=(2,2)))
model.add(BatchNormalization())
model.add(Flatten())
model.add(Dense(9216, activation='relu',name='features'))
model.add(Dropout(0.4))
model.add(Dense(4096, activation='relu'))
model.add(Dense(4096, activation='relu'))
model.add(Dense(1000, activation='relu'))
model.add(Dense(NUM_CLASSES, activation='softmax'))
model.summary()

from keras.utils import plot_model
plot_model(model, to_file='model.png')

filename="best_weights.h5"
filename2="weights.{epoch:02d}-{val_loss:.2f}.hdf5"




## define the model with input layer and output layer
# Training

checkpoints = []

if not os.path.exists('Results/'):
    os.makedirs('Results/')

checkpoints.append(ModelCheckpoint('Results/'+filename,
                                   monitor='val_acc',
                                   verbose=1,
                                   save_best_only=True,
                                   save_weights_only=True,
                                   mode='auto',
                                   period=1))

checkpoints.append(ModelCheckpoint('Results/'+filename2,
                                   monitor='val_acc',
                                   verbose=1,
                                   save_best_only=False,
                                   save_weights_only=True,
                                   mode='auto',
                                   period=20))

checkpoints.append(TensorBoard(log_dir='Results/TensorBoardLogs',
                               histogram_freq=0,
                               write_graph=True,
                               write_images=False,
                               embeddings_freq=0,
                               embeddings_layer_names=['features'],
                               embeddings_metadata='metadata.tsv'))

checkpoints.append(keras.callbacks.EarlyStopping(monitor='val_acc', mode='max', min_delta=0, patience=10))
checkpoints.append(keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=10, verbose=0, mode='auto', min_delta=0.0001, cooldown=0, min_lr=0))
checkpoints.append(CSVLogger('Results/log.csv'))
# Training
## define the model with input layer and output layer
# Training


#Compilation
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
# augmentation
datagen = ImageDataGenerator(
    featurewise_center=True,
    featurewise_std_normalization=True,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True)

#training

NUM_EPOCHS = 100
history= model.fit(datagen.flow(x_train, y_train, batch_size=32),
          steps_per_epoch=len(x_train) / 32,
          validation_data=(x_val,y_val),
          batch_size= BATCH_SIZE,
          shufffle = true,
          epochs =NUM_EPOCHS,
          callbacks=checkpoints)

#for fancy plotting of loss functions
# there is also an option of tensorflow visualization


import matplotlib.pyplot as plt
import numpy
print(history.history.keys())

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
