# Computational-Fluid-Dynamics-Machine-Learning-Examples
This repo contains tutorial type programs showing some basic ways Neural Networks can be applied to CFD. The purpose of this is to give those who are familiar with CFD but not Neural Networks a few very simple examples of applications. In particular, there is an example for predicting drag from the boundary conditions as well as predicting the velocity and pressure field from the boundary conditions.

The Neural Network code is written with the popular and easy to use [Keras](https://keras.io/) library. [OpenLB](http://optilb.org/openlb/) is used to generate the simulation data needed for training.

Here are figures of the two networks to train.

![alt tag](https://github.com/loliverhennigh/Computational-Fluid-Dynamics-Machine-Learning-Examples/blob/master/figs/drag-predictor-network.jpg)

![alt tag](https://github.com/loliverhennigh/Computational-Fluid-Dynamics-Machine-Learning-Examples/blob/master/figs/steady-state-flow-predicting-networ.jpg)

# Needed Install Stuff

You will need the following packages to run all the code. Mpi stuff for OpenLB and Keras for the Neural Networks. Starting from a fresh image of Ubuntu 16.04 the following should meet all dependencies.

```
sudo apt-get update
sudo apt-get install g++ openmpi-bin openmpi-doc libopenmpi-dev make python-vtk python-tk
sudo pip install tqdm keras tensorflow matplotlib
```

Note, if you want the gpu version of Tensorflow you need to install `tensorflow-gpu` and follow the instructions [here](https://www.tensorflow.org/install/install_linux). Also, depending how python vtk is install it can cause problems. If the above instructions are followed without a prior install of vtk then there should be no problem.

# How To Generate Train Data

This repo uses OpenLB to generate the train and test set of simulation data. To setup the library run
```
./setup_olb.sh
```
This will download and compile the simulator. Now to generate the train and test set run
```
python make_dataset.py
```
This program will generate 2,000 examples of steady state flow around a cylinder at various positions and radii (simple as possible). On a i7 processor it takes about 1 hour and 2 hours on an i5. Keep in mind that it is multithreaded and runs several simulations at the same time. If you notice your machines cpu is not maxed out you can adjust the `num_que` parameter to make it go faster. You can also change `num_runs` to change how many simulations to run.

# How To Train Networks


To train a network in predicting the steady state flow velocity vector field and pressure field run
```
keras_steady_flow_predictor.py
```
For the drag predicting network run
```
keras_drag_predictor.py
```

Check these scripts and the above images for more info and explanation of what is happening.

# Results

Running the steady state flow predictor produces images like these. 

![alt tag](https://github.com/loliverhennigh/Computational-Fluid-Dynamics-Machine-Learning-Examples/blob/master/figs/steady_state_flow_1.png)
![alt tag](https://github.com/loliverhennigh/Computational-Fluid-Dynamics-Machine-Learning-Examples/blob/master/figs/steady_state_flow_2.png)
![alt tag](https://github.com/loliverhennigh/Computational-Fluid-Dynamics-Machine-Learning-Examples/blob/master/figs/steady_state_flow_3.png)
![alt tag](https://github.com/loliverhennigh/Computational-Fluid-Dynamics-Machine-Learning-Examples/blob/master/figs/steady_state_flow_4.png)

Once trained, the drag predicting network has an average mean squared error of 0.72. Given the boundary it is able to reasonable predict the drag. Here are 3 predictions for examples.

![alt tag](https://github.com/loliverhennigh/Computational-Fluid-Dynamics-Machine-Learning-Examples/blob/master/figs/drag_1.png)

true drag is     : [ 10.7171]
predicted drag is: [ 10.45950699]


![alt tag](https://github.com/loliverhennigh/Computational-Fluid-Dynamics-Machine-Learning-Examples/blob/master/figs/drag_2.png)

true drag is     : [ 7.64211]
predicted drag is: [ 6.81015682]

![alt tag](https://github.com/loliverhennigh/Computational-Fluid-Dynamics-Machine-Learning-Examples/blob/master/figs/drag_3.png)

true drag is     : [ 6.08601]
predicted drag is: [ 5.85990286]

# Discussion

While there has been relatively little work applying Neural Networks to Computational Fluid Dynamics, there are many interesting applications. If you found these examples helpful you can check out https://github.com/loliverhennigh/Steady-State-Flow-With-Neural-Nets or https://github.com/loliverhennigh/Phy-Net for other applications. I also am compiling a comprehensive list of papers on the subject [here](https://github.com/loliverhennigh/Computational-Physics-and-Machine-Learning-Reading-List).

