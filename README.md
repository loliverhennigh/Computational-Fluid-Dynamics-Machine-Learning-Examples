# Computational-Fluid-Dynamics-Machine-Learning-Examples
This repo contains some tutorial type programs showing some basic ways machine learning can be applied to CFD. The purpose of this is to give those who are familar with CFD but not Neural Networks a few very simple examples of applications. In particular, there is an e

The Neural Network code is written with the popular and easy to use [Keras](https://keras.io/) library. [OpenLB](http://optilb.org/openlb/) is used to generate the simulation data needed for training.

# Needed Install Stuff

You will need the following packages to run all the code. Mpi stuff for OpenLB and Keras for the Neural Networks. Starting from a fresh image of Ubuntu 16 the following should meet all dependencies.

```
sudo apt-get update
sudo apt-get install g++ openmpi-bin openmpi-doc libopenmpi-dev make python-vtk
sudo pip install tqdm keras tensorflow
```

Note, if you want the gpu version of Tensorflow you need to install `tensorflow-gpu` and follow the instructions [here](https://www.tensorflow.org/install/install_linux).

# How To Generate Train Data

This repo realize on OpenLB to generate the train and test set of simulation data. To setup the library run
```
./setup_olb.sh
```
This will download and compile the simulator. Now to generate the train and test set run
```
python make_dataset.py
```
This program will generate 3,000 examples of steady state flow around a cylinder at various positions and radie. On a i7 processor it takes about 1 hour and 2 hours on an i5. Keep in mind that it is multithreaded and runs several simulations at the same time. If you notice your machines cpu is not maxed out you can adjust the `num_que` parameter to make it go faster. You can also change `num_runs` to change how many simulations to run. 

# How To Train Networks


To train a network in predicting the steady state flow velocity vector field and preassure field run
```
keras_steady_flow_predictor.py
```

# Results




# Discussion



