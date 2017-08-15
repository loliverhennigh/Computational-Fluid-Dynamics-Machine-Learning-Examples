# Computational-Fluid-Dynamics-Machine-Learning-Examples
This repo contains some tutorial type programs showing some basic ways machine learning can be applied to CFD. The purpose being to give those who are familar with CFD but not Neural Networks a few very simple examples of applications. 

The Neural Network code is written with the popular and easy to use [Keras](https://keras.io/) library. [OpenLB](http://optilb.org/openlb/) is used to generate the simulation data needed for training.

# Needed Install Stuff



# How To Generate Train Data

This repo realize on OpenLB to generate the train and test set of simulation data. To setup the library run
```
./setup_olb.sh
```
This will download and compile the simulator. Now to generate the train and test set run
```
python make_dataset.py
```
This program is multithreaded and on a i7 processor it takes about 1 hour and 2 hours on an i5

# How To Train Networks

The purpose of this tutorial is to give a brief look at how Neural Networks can be applied to Computational Fluid Dynamics

To train a network in predicting the steady state flow velocity vector field and preassure field run
```
keras_steady_flow_predictor.py
```

# Results


# Discussion



