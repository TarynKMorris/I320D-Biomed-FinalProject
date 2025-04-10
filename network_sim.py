#  File: network_sim.py
#  Description: Initializes classes for oop approach to simulating networks
#  Code based on class code for CS 313 E, 
#  https://medium.com/data-science/simulation-106-modeling-
#  information-diffusion-and-social-contagion-with-networks-7c1184004889

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import imageio.v3 as iio

class Network (object):
  def __init__ (self):
    G = nx.Graph()
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
    self.check_visibility(index)

  def check_visibility(self, index):
    n = self.G.nodes[index]
    if n['discontent'] >= n['threshold']:
      n['isvisible'] = True
    #print('visibility checked')
  
  def change_discontent(self, index, amt):
    n = self.G.nodes[index]
    n['discontent'] += amt
    self.check_visibility(index)

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

def generate_individial_stats(amt):
  base_discontent = 5 * np.random.randn(amt) + 10
  threshold = 10 * np.random.randn(amt) + 20
  return base_discontent, threshold

def create_labels(G):
  labels = {}
  for inx, dict in G.nodes.data(): 
    labels[inx] = f"{dict['discontent']:.0f}/{dict['threshold']:.0f}"
  return labels

def create_test_nw(num_nodes, avg_degree):
  network = Network()
  discontent, threshold = generate_individial_stats(num_nodes)
  for d,t in zip(discontent,threshold):
    network.add_node(d,t)
  create_connections(network, avg_degree)
  return network

def get_color(G):
    color_dict = dict({True:"red",False:"blue"})
    color = list(dict(G.nodes(data="isvisible")).values())
    color = [color_dict[i] for i in color]
    return color

def create_connections(network,num):
  nodes = list(network.G.nodes)
  for i in range(len(nodes) * num):
    if i == 0: 
      node1 = nodes[0]
    else:
      node1 = np.random.choice(nodes)
    node2 = np.random.choice(nodes)
    
    if node1 != node2:
      network.add_undirected_edge(node1,node2)

def main():
  print('Start')
  network = create_test_nw(100, 3)
  #print(nx.average_neighbor_degree(network.G))
  colors = get_color(network.G)
  nx.draw(network.G, node_color = colors)
  plt.show()
  #freq = nx.degree_histogram(network.G), 
  #plt.boxplot(freq, showmeans= True)
  #plt.show()
  print(nx.density(network.G))
  print("Finished")

def create_network():
  # Creates network based on input
  print("Not supported")

if __name__ == "__main__":
    main()

