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
    prev_viz = n['isvisible']
    n['discontent'] += amt
    self.check_visibility(index)
    if prev_viz != n['isvisible']:
      print(f"{index} is now visible")

  # add weighted undirected edge to graph
  def add_undirected_edge (self, start, finish, weight = 1):
    self.G.add_edge(start, finish)
    self.G[start][finish]['weight'] = weight
  
  def observe_discontent(self, index):
    peer_discontent = []
    for nbr_idx in self.G[index]:
      nbr = self.G.nodes[nbr_idx]
      #print(node, nx.get_node_attributes(self.G, node))
      if nbr['isvisible']:
        #print(nbr, nbr['discontent'],nbr['threshold'])
        influence = nbr['discontent'] * self.G[index][nbr_idx]['weight']
        peer_discontent.append(influence)
    if len(peer_discontent) >= 1:
      avg_discontent = np.mean(peer_discontent)
      #print("Avg discontent", f"{avg_discontent:.0f}")
      #print(self.G.nodes[index]['discontent'])
      self.change_discontent(index, avg_discontent)
      #print(self.G.nodes[index]['discontent'])
      

  def propogate_discontent(self):
    # discontent = discontent + weighted average of peers
    visible = [x for x,y in self.G.nodes(data=True) if y['isvisible']]
    for node in visible:
      print(f"{node} is visible")
      for nbr in self.G[node]:
        print(f'{nbr} neighbors {node}')
        self.observe_discontent(nbr)

def generate_individial_stats(amt):
  base_discontent = 10 * np.random.randn(amt) + 5
  threshold = 10 * np.random.randn(amt) + 30
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
  network.propogate_discontent()
  colors = get_color(network.G)
  nx.draw(network.G, node_color = colors)
  plt.show()

  #freq = nx.degree_histogram(network.G), 
  #plt.boxplot(freq, showmeans= True)
  #plt.show()
  #print(nx.number_of_nodes(network.G)/nx.number_of_edges(network.G))
  print("Finished")

def create_network():
  # Creates network based on input
  print("Not supported")

if __name__ == "__main__":
    main()

