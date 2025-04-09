#  File: network_sim.py
#  Description: Initializes classes for oop approach to simulating networks
#  Code based on class code for CS 313 E

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

class Vertex (object):
  def __init__ (self, label, discontent, threshold):
    self.discontent = discontent
    self.threshold = threshold
    self.label = label
    self.isvisible = False
    self.check_visibility()

  # determine the label of the vertex
  def get_label (self):
    return self.label
  
  # Change level of discontent, check effect on visibility
  def change_discontent(self, amt):
    self.discontent += amt
    self.check_visibility()

  # Check if discontent is visible to others
  def check_visibility (self):
    if self.discontent >= self.threshold:
      self.isvisible = True
    #print("Checked Visibility")

  # string representation of the vertex
  def __str__ (self):
    info = f"{self.label}: {self.discontent:.0f}/{self.threshold:.0f}"
    if self.isvisible:
      info = "(" + info + ")"
    return info
  
def create_test_nw():
  base_discontent = 5 * np.random.randn(14) + 10
  threshold = 10 * np.random.randn(14) + 20
  labels = ['Node' + str(i) for i in range(14)]
  verticies = [Vertex(label,d,t) for label, d, t in zip(labels,base_discontent,threshold)]
  #print('num:', len(labels), len(base_discontent), len(threshold))
  nw = nx.Graph()
  nw.add_nodes_from(verticies)
  return nw

def main():
  print('Start')
  nw = create_test_nw()
  colors = []
  for node in nw:
    if node.isvisible:
      colors.append('red')
    else:
      colors.append('blue')
  nx.draw(nw, node_color = colors,with_labels = True)
  plt.show()
    
  print("Finished")

def create_network():
  # Creates network based on input
  print("Not supported")

if __name__ == "__main__":
    main()

