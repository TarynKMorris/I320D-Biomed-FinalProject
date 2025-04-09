#  File: network_sim.py
#  Description: Initializes classes for oop approach to simulating networks
#  Code based on class code for CS 313 E

import matplotlib.pyplot as plt
import networkx as nx

class Vertex (object):
  def __init__ (self, label, discontent, threshold):
    self.discontent = discontent
    self.threshold = threshold
    self.label = label
    self.isvisible = False

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
    print("Checked Visibility")

  # string representation of the vertex
  def __str__ (self):
    info = f"{self.label}: {self.discontent}/{self.threshold}"
    return info
  

def main():
  print('Start')
  G = nx.petersen_graph()
  subax1 = plt.subplot(121)
  nx.draw(G, with_labels=True, font_weight='bold')
  subax2 = plt.subplot(122)
  nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
  plt.show()
  network = nx.Graph()
  node1 = Vertex('friend1', 5, 20)
  node2 = Vertex('friend2', 10, 20)
  network.add_edge(node1,node2)
  nx.draw(network)
  plt.draw()  # pyplot draw()
  plt.show()
  print("Finished")

def create_network():
  # Creates network based on input
  print("Not supported")

if __name__ == "__main__":
    main()

