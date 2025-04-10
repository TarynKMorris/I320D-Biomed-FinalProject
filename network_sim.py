#  File: network_sim.py
#  Description: Initializes classes for oop approach to simulating networks
#  Code based on class code for CS 313 E

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import imageio.v3 as iio

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


class Network (object):
  def __init__ (self):
    G = nx.DiGraph()
    self.G = G

  # check if a vertex is already in the graph
  def has_vertex (self, label):
    nVert = len (self.Vertices)
    for i in range (nVert):
      if (label == (self.Vertices[i]).get_label()):
        return True
    return False
  
  def add_node(self,d,t):
    index = len(self.G.nodes)
    self.G.add_node(index,
                     discontent = d,
                     threshold = t,
                     isvisible = False)
    #print('created')
    self.check_visibility(self.G.nodes[index])

  def check_visibility(self, n):
    if n['discontent'] >= n['threshold']:
      n['isvisible'] = True
    #print('visibility checked')

  # add weighted undirected edge to graph
  def add_undirected_edge (self, start, finish, weight = 1):
    self.G.add_edge(start, finish)
    self.G[start][finish]['weight'] = weight

  # return all vertices adjacent to vertex v (index)
  def get_adj_vertices (self, v):
    nVert = len (self.Vertices)
    adj = []
    for i in range (nVert):
      if (self.adjMat[v][i] > 0):
        adj.append(i)
    if len(adj) != 0:
      return adj
    return -1
  
  def update_discontent(self, v ):
    # discontent = discontent + weighted average of peers
    nVert = len (self.Vertices)
    peer_discontent = []
    for i in range (nVert):
      peer = self.Vertices[i]
      peer.check_visibility()
      peer_weight =  self.adjMat[v][i]
      if peer_weight > 0 and peer.isvisible:
        influence = self.adjMat[v][i] * peer.discontent
        peer.append(influence) 

  def print_adj_matrix(self):
    print("Adjacency matrix:")

    for v in range(len(self.Vertices)):
      row = ""
      for i in range(len(self.adjMat[v])):
        row += str(self.adjMat[v][i])
      print(row)

def generate_individial_stats(amt):
  base_discontent = 5 * np.random.randn(amt) + 10
  threshold = 10 * np.random.randn(amt) + 20
  return base_discontent, threshold

def create_test_nw():
  base_discontent, threshold = generate_individial_stats(14)
  labels = ['Node' + str(i) for i in range(14)]
  verticies = [Vertex(label,d,t) for label, d, t in zip(labels,base_discontent,threshold)]
  #print('num:', len(labels), len(base_discontent), len(threshold))
  nw = nx.Graph()
  nw.add_nodes_from(verticies)
  return nw

def get_color(graph):
    color_dict = dict({True:"red",False:"blue"})
    color = list(dict(graph.nodes(data="isvisible")).values())
    color = [color_dict[i] for i in color]
    return color

def main():
  print('Start')
  # nw = create_test_nw()
  # colors = []
  # for node in nw:
  #   if node.isvisible:
  #     colors.append('red')
  #   else:
  #     colors.append('blue')
  # nx.draw(nw, node_color = colors,with_labels = True)
  # plt.show()
  network = Network()
  discontent, threshold = generate_individial_stats(10)
  for d,t in zip(discontent,threshold):
    network.add_node(d,t)
  colors = get_color(network.G)
  nx.draw(network.G, node_color = colors)
  plt.show()
  print("Finished")

def create_network():
  # Creates network based on input
  print("Not supported")

if __name__ == "__main__":
    main()

