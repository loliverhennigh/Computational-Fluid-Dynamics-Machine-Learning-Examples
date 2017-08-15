'''Trains a simple convnet on the MNIST dataset.

Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''

# keras import stuff
import keras
from keras.models import Model
from keras.layers import Input, concatenate, Conv2D, MaxPooling2D, Conv2DTranspose
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
train_steady_flows = dataset.steady_flows[0:dataset.split_line]
test_geometries = dataset.geometries[dataset.split_line:-1]
test_steady_flows = dataset.steady_flows[dataset.split_line:-1]

# reshape into single np array
train_geometries = np.stack(train_geometries, axis=0)
train_steady_flows = np.stack(train_steady_flows, axis=0)
test_geometries = np.stack(test_geometries, axis=0)
test_steady_flows = np.stack(test_steady_flows, axis=0)

# print dataset values
print('geometry shape:', train_geometries.shape[1:])
print('steady flow shape:', train_steady_flows.shape[1:])
print(train_geometries.shape[0], ' train samples')
print(test_geometries.shape[0], ' test samples')

# construct model
inputs = Input(train_geometries.shape[1:])
conv1 = Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
conv1 = Conv2D(32, (3, 3), activation='relu', padding='same')(conv1)
pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)

conv2 = Conv2D(64, (3, 3), activation='relu', padding='same')(pool1)
conv2 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv2)
pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)

conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool2)
conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv3)
pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)

conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(pool3)
conv4 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv4)
pool4 = MaxPooling2D(pool_size=(2, 2))(conv4)

conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(pool4)
conv5 = Conv2D(512, (3, 3), activation='relu', padding='same')(conv5)

up6 = concatenate([ZeroPadding2D(((1,0),(1,0)))(Conv2DTranspose(256, (2, 2), strides=(2, 2), padding='same')(conv5)), conv4], axis=3)
conv6 = Conv2D(256, (3, 3), activation='relu', padding='same')(up6)
conv6 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv6)

up7 = concatenate([ZeroPadding2D(((1,0),(1,0)))(Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(conv6)), conv3], axis=3)
conv7 = Conv2D(128, (3, 3), activation='relu', padding='same')(up7)
conv7 = Conv2D(128, (3, 3), activation='relu', padding='same')(conv7)

up8 = concatenate([ZeroPadding2D(((0,0),(1,0)))(Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(conv7)), conv2], axis=3)
conv8 = Conv2D(64, (3, 3), activation='relu', padding='same')(up8)
conv8 = Conv2D(64, (3, 3), activation='relu', padding='same')(conv8)

up9 = concatenate([ZeroPadding2D(((0,0),(1,0)))(Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(conv8)), conv1], axis=3)
conv9 = Conv2D(32, (3, 3), activation='relu', padding='same')(up9)
conv9 = Conv2D(32, (3, 3), activation='relu', padding='same')(conv9)

conv10 = Conv2D(3, (1, 1), activation='linear')(conv9)

model = Model(inputs=[inputs], outputs=[conv10])

model.compile(loss=keras.losses.mean_squared_error,
              optimizer=keras.optimizers.Adam(lr=1e-4),
              metrics=['MSE'])

# train model
model.fit(train_geometries, train_steady_flows,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(test_geometries, test_steady_flows))

# eval model on test set
predicted_steady_flow = model.predict(test_geometries, batch_size=batch_size)
for i in xrange(predicted_steady_flow.shape[0]):
  # plot predicted vs true flow
  velocity_image = np.concatenate([predicted_steady_flow[i,:,:,0], test_steady_flows[i,:,:,0], test_geometries[i,:,:,0]/10.0], axis=1)
  plt.imshow(velocity_image)
  plt.show()
  # plot predicted vs true pressure
  velocity_image = np.concatenate([predicted_steady_flow[i,:,:,2], test_steady_flows[i,:,:,2], test_geometries[i,:,:,0]/10.0], axis=1)
  plt.imshow(velocity_image)
  plt.show()
 



