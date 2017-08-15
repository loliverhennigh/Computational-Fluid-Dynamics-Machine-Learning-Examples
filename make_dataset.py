
import os
import numpy as np
import xml.etree.cElementTree as ET
from tqdm import *
import subprocess
from Queue import Queue
from threading import Thread

# Que up simulations to run
simulation_queue = Queue(20)
def worker():
  while True:
    [sim_cmd, rm_cmd] = simulation_queue.get()
    with open(os.devnull, 'w') as devnull:
      try: # maybe remove old simulation data
        subprocess.check_call(rm_cmd.split(' '), stdout=devnull, stderr=devnull)
      except:
        pass
      subprocess.check_call(sim_cmd.split(' '), stdout=devnull, stderr=devnull)
      simulation_queue.task_done()

# make thread
for i in xrange(4):
  t = Thread(target=worker)
  t.daemon = True
  t.start()
 
# number of simulations
num_runs = 300

# create xml file and run simulation
for i in tqdm(xrange(num_runs)):
  # make random pos and radius for circle
  rand_x = np.random.uniform(0.20, 1.0)
  rand_radius = np.random.uniform(0.05, 0.15)
  rand_y = np.random.uniform(0.0 + rand_radius + 0.01, 0.41 - rand_radius - 0.01)

  # save data into xml param file that olb will read
  root = ET.Element("Param")
  doc = ET.SubElement(root, "Mesh")
  ET.SubElement(doc, "x_pos").text  = str(rand_x)
  ET.SubElement(doc, "y_pos").text  = str(rand_y)
  ET.SubElement(doc, "radius").text = str(rand_radius)
  paths = ET.SubElement(root, "save_path")
  ET.SubElement(paths, "dirname").text = os.path.abspath('.') + "/data/simulation_data/runlog_" + str(i).zfill(5) + "/"
  tree = ET.ElementTree(root)
  tree.write("./data/xml_runs/run_" + str(i).zfill(5) + ".xml")

  # run simulation (rm is already there)
  sim_cmd = "./cylinder2d/cylinder2d ./data/xml_runs/run_" + str(i).zfill(5) + ".xml"
  rm_cmd = "rm -r " + os.path.abspath('.') + "/data/simulation_data/runlog_" + str(i).zfill(5)
  simulation_queue.put([sim_cmd, rm_cmd])

# start que
simulation_queue.join()

