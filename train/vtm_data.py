
import numpy as np
import vtk
from vtk.util.numpy_support import *
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import glob

class VTK_data:
  def __init__(self, base_dir, train_test_split=.8):

    # base dir where all the xml files are
    self.base_dir = base_dir

    # lists to store the datasets
    self.geometries    = []
    self.steady_flows = []
    self.drag_vectors = []

    # train vs test split (numbers under this value are in train, over in test)
    self.train_test_split = train_test_split
    self.split_line = 0

  def load_data(self): 
    # reads in all xml data into lists

    # get list of all xml file in dataset
    xml_files = glob.glob(self.base_dir + "/xml_runs/*.xml")

    for f in xml_files:

      # parse xml file
      tree = ET.parse(f)
      root = tree.getroot()
      dir_name = root.find('save_path').find('dirname').text
     
      # get needed filenames
      geometry_file = dir_name + "vtkData/geometry_iT0000000.vtm"
      steady_flow_file = glob.glob(dir_name + "/vtkData/data/*.vtm")
      if len(steady_flow_file) == 0:
        continue
      else:
        steady_flow_file = steady_flow_file[0]
      drag_vector_file = dir_name + "gnuplotData/data/drag.dat"
      
      # read file for geometry
      reader = vtk.vtkXMLMultiBlockDataReader()
      reader.SetFileName(geometry_file)
      reader.Update()
      data = reader.GetOutput()
      data_iterator = data.NewIterator()
      img_data = data_iterator.GetCurrentDataObject() 
      img_data.Update()
      point_data = img_data.GetPointData()
      array_data = point_data.GetArray(0)
      np_array = vtk_to_numpy(array_data)
      img_shape = img_data.GetWholeExtent()
      np_shape = [img_shape[3] - img_shape[2] + 1, img_shape[1] - img_shape[0] + 1, 1]
      geometry_array = np_array.reshape(np_shape)
      if np.isnan(geometry_array).any():
        continue

      # read file for steady state flow
      reader = vtk.vtkXMLMultiBlockDataReader()
      reader.SetFileName(steady_flow_file)
      reader.Update()
      data = reader.GetOutput()
      data_iterator = data.NewIterator()
      img_data = data_iterator.GetCurrentDataObject() 
      img_data.Update()
      point_data = img_data.GetPointData()
      velocity_array_data = point_data.GetArray(0)
      pressure_array_data = point_data.GetArray(1)
      velocity_np_array = vtk_to_numpy(velocity_array_data)
      pressure_np_array = vtk_to_numpy(pressure_array_data)
      img_shape = img_data.GetWholeExtent()
      velocity_np_shape = [img_shape[3] - img_shape[2] + 1, img_shape[1] - img_shape[0] + 1, 2]
      pressure_np_shape = [img_shape[3] - img_shape[2] + 1, img_shape[1] - img_shape[0] + 1, 1]
      velocity_np_array = velocity_np_array.reshape(velocity_np_shape)
      pressure_np_array = pressure_np_array.reshape(pressure_np_shape)
      steady_flow_array = np.concatenate([velocity_np_array, pressure_np_array], axis=2)
      if np.isnan(steady_flow_array).any():
        continue

      # read file for drag vector
      reader = open(drag_vector_file, "r")
      drag_values = reader.readlines()
      drag_array = np.zeros((len(drag_values)))
      for i in xrange(len(drag_values)):
        values = drag_values[i].split(' ')
        drag_array[i] = float(values[1])
      if np.isnan(drag_array).any():
        continue

      # if no nans then store
      self.geometries.append(geometry_array)
      self.steady_flows.append(steady_flow_array)
      self.drag_vectors.append(drag_array)

    self.split_line = int(self.train_test_split * len(self.geometries))

  def minibatch(self, train=True, batch_size=32, batch_type="flow"):
    batch_boundary = []
    batch_data = []
    for i in xrange(batch_size): 
      if train:
        sample = np.random.randint(0, self.split_line)
      else:
        sample = np.random.randint(self.split_line, len(self.boundarys))
      batch_boundary.append(self.geometries[sample])
      if batch_type == "flow":
        batch_data.append(self.steady_flows[sample])
      elif batch_type == "drag":
        batch_data.append(self.drag_vectors[sample])
    return batch_boundary, batch_data

"""
dataset = VTK_data("./xml_runs")
dataset.load_data()
batch_boundary, batch_data = dataset.minibatch(batch_type="flow")
for i in xrange(32):
  plt.imshow(batch_boundary[i][:,:,0])
  plt.show()
  plt.imshow(batch_data[i][:,:,0])
  #plt.plot(batch_data[i])
  plt.show()
""" 
