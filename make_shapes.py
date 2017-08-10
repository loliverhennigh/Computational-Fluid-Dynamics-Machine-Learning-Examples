
import os
import numpy as np
import xml.etree.cElementTree as ET
from tqdm import *

num_runs = 1000

for i in tqdm(xrange(num_runs)):
  rand_x = np.random.uniform(0.15, 1.0)
  rand_y = np.random.uniform(0.0, 0.41)
  rand_radius = np.random.uniform(0.05, 0.15)

  root = ET.Element("Param")
  doc = ET.SubElement(root, "Mesh")
  ET.SubElement(doc, "x_pos").text  = str(rand_x)
  ET.SubElement(doc, "y_pos").text  = str(rand_y)
  ET.SubElement(doc, "radius").text = str(rand_radius)

  paths = ET.SubElement(root, "save_path")
  ET.SubElement(paths, "dirname").text = "./tmp/runlog_" + str(i).zfill(5) + "/"

  tree = ET.ElementTree(root)
  tree.write("xml_runs/run_" + str(i).zfill(5) + ".xml")

  os.system("./cylinder2d xml_runs/run_" + str(i).zfill(5) + ".xml > /dev/null")

