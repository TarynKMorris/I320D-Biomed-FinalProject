#  File: network_sim.py
#  Description: Initializes classes for oop approach to simulating networks
#  Code based on class code for CS 313 E, 
#  https://medium.com/data-science/simulation-106-modeling-
#  information-diffusion-and-social-contagion-with-networks-7c1184004889

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import imageio.v3 as iio
import os
import shutil

# Adapted from Le Nguyen Medium article
# Make helper functions
def makeGif(networks, name, pos):
  os.mkdir('frames')
  try: 
    counter=0
    images = []
    for i in range(0,len(networks)):
      plt.figure(figsize = (8,8))

      color = get_color(networks[i])
      nx.draw(networks[i],  node_color = color, pos = pos)
      plt.savefig("frames/" + str(counter)+ ".png")
      images.append(iio.imread("frames/" + str(counter)+ ".png"))
      counter += 1
      plt.close()
    iio.imwrite(name, images, loop = 0, duration = 1)
  finally:
    shutil.rmtree('frames')

class Network (object):
  def __init__ (self):
    G = nx.Graph()
    self.G = G
  
  # Add node
  def add_node(self,d,t):
    index = len(self.G.nodes)
    self.G.add_node(index,
                     discontent = d,
                     threshold = t,
                     isvisible = False)
    self.check_visibility(index)

  # add weighted undirected edge to graph
  def add_undirected_edge (self, start, finish, weight = 1):
    self.G.add_edge(start, finish)
    self.G[start][finish]['weight'] = weight

  # Update visibility of node
  def check_visibility(self, index):
    n = self.G.nodes[index]
    if n['discontent'] >= n['threshold']:
      n['isvisible'] = True
    #print('visibility checked')
  
  # change discontent of node
  def change_discontent(self, index, amt):
    n = self.G.nodes[index]
    prev_viz = n['isvisible']
    n['discontent'] += amt
    self.check_visibility(index)
    # if prev_viz != n['isvisible']:
      # print(f"{index} is now visible")
  
  def simulate_exhaustion(self):
    # method to simulate people un-becoming visibly discontent?
    # Exhausted bool? If exhausted, no longer affects others?
    print("Not set up")
  
  # Update node discontent based on surroundings
  def observe_discontent(self, index):
    peer_discontent = []
    for nbr_idx in self.G[index]:
      nbr = self.G.nodes[nbr_idx]
      #print(node, nx.get_node_attributes(self.G, node))
      if nbr['isvisible']:
        #print(nbr, nbr['discontent'],nbr['threshold'])
        influence = nbr['discontent'] * self.G[index][nbr_idx]['weight']
      else:
        influence = 0
      peer_discontent.append(influence)
    if len(peer_discontent) >= 1:
      avg_discontent = np.mean(peer_discontent)
      #print("Avg discontent", f"{avg_discontent:.0f}")
      #print(self.G.nodes[index]['discontent'])
      self.change_discontent(index, avg_discontent)
      #print(self.G.nodes[index]['discontent'])   

  # Simulate effect of discontent on neighbors
  def propogate_discontent(self):
    # discontent = discontent + weighted average of peers
    visible = [x for x,y in self.G.nodes(data=True) if y['isvisible']]
    for node in visible:
      # print(f"{node} is visible")
      for nbr in self.G[node]:
        # print(f'{nbr} neighbors {node}')
        self.observe_discontent(nbr)

######################################

def generate_individial_stats(amt):
  base_discontent = 5 * np.random.randn(amt) + 10
  threshold = 10 * np.random.randn(amt) + 50
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
  network = create_test_nw(500, 3)
  network.G.nodes[0]['isvisible'] = True
  colors = get_color(network.G)
  pos = nx.kamada_kawai_layout(network.G)
  
  #Propogate idea
  visible = []
  networks = [network.G.copy()]
  for i in range(0,50):
    network.propogate_discontent()
    visible.append(sum(list(dict(network.G.nodes(data="isvisible")).values())))
    networks.append(network.G.copy())
  
  # Save gif
  makeGif(networks, "contagion.gif", pos)

  # Plot contagion curve
  plt.figure()
  t = np.arange(0,len(visible),1)
  plt.plot(t,visible)
  plt.xlabel("Time")
  plt.ylabel("Visibly Discontent Members")
  plt.title("Discontent Contagion Curve")
  plt.show()
  print("Finished")

if __name__ == "__main__":
    main()

