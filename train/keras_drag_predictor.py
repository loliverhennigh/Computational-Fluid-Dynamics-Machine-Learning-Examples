'''Trains a simple convnet on the MNIST dataset.

Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''

# keras import stuff
import keras
from keras.models import Model
from keras.layers import Input, concatenate, Conv2D, MaxPooling2D, Conv2DTranspose, Dense, Dropout, Flatten
from keras.layers.convolutional import ZeroPadding2D
from keras import backend as K

# vtm dataset maker
from vtm_data import VTK_data

# numpy and matplot lib
import numpy as np
import matplotlib.pyplot as plt

# training params
batch_size = 32
epochs = 100 # number of times through training set

# load dataset
dataset = VTK_data("../data")
dataset.load_data()

# get train and test split
train_geometries = dataset.geometries[0:dataset.split_line]
train_drag_vectors = [value[-1:] for value in dataset.drag_vectors[0:dataset.split_line]]
test_geometries = dataset.geometries[dataset.split_line:-1]
test_drag_vectors = [value[-1:] for value in dataset.drag_vectors[dataset.split_line:-1]]

# reshape into single np array
train_geometries = np.stack(train_geometries, axis=0)
train_drag_vectors = np.stack(train_drag_vectors, axis=0)
test_geometries = np.stack(test_geometries, axis=0)
test_drag_vectors = np.stack(test_drag_vectors, axis=0)

# print dataset values
print('geometry shape:', train_geometries.shape[1:])
print('drag shape:', train_drag_vectors.shape[1:])
print(train_geometries.shape[0], ' train samples')
print(test_geometries.shape[0], ' test samples')

# construct model
inputs = Input(train_geometries.shape[1:])
conv1 = Conv2D(4, (3, 3), activation='relu', padding='same')(inputs)
conv1 = Conv2D(4, (3, 3), activation='relu', padding='same')(conv1)
pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

conv2 = Conv2D(8, (3, 3), activation='relu', padding='same')(pool1)
conv2 = Conv2D(8, (3, 3), activation='relu', padding='same')(conv2)
pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

conv3 = Conv2D(16, (3, 3), activation='relu', padding='same')(pool2)
conv3 = Conv2D(16, (3, 3), activation='relu', padding='same')(conv3)
pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

conv4 = Conv2D(64, (3, 3), activation='relu', padding='same')(pool3)
conv4 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv4)
pool4 = MaxPooling2D(pool_size=(2, 2))(conv4)

flat4 = Flatten()(conv4)
flat5 = Dense(512, activation='relu')(flat4)

flat5_dropout = Dropout(0.5)(flat5)
out = Dense(1, activation='linear')(flat5_dropout)

model = Model(inputs=[inputs], outputs=[out])

model.compile(loss=keras.losses.mean_squared_error,
              optimizer=keras.optimizers.Adam(lr=3e-5),
              metrics=['MSE'])

# train model
model.fit(train_geometries, train_drag_vectors,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(test_geometries, test_drag_vectors))

# eval model on test set
predicted_drag_vectors = model.predict(test_geometries, batch_size=batch_size)
for i in xrange(predicted_drag_vectors.shape[0]):
  # plot predicted vs true flow
  print("geometry in plot")
  print("true drag is     : " + str(test_drag_vectors[i]))
  print("predicted drag is: " + str(predicted_drag_vectors[i]))
  plt.imshow(test_geometries[i,:,:,0])
  plt.show()

 



