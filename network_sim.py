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
  def __init__ (self, media = 0, media_accuracy = .5,
                 efficacy = .8, homophily = .5,
                 percieved_cost = 10):
    G = nx.Graph(media = media,
                 media_accuracy = media_accuracy,
                 efficacy = efficacy,
                 homophily = homophily,
                 percieved_cost = percieved_cost)
    self.G = G
  
  # Add node
  def add_node(self,d,t,b = 0,r = 0):
    index = len(self.G.nodes)
    self.G.add_node(index,
                     discontent = d,
                     threshold = t,
                     burnout = b,
                     resistance = r,
                     isvisible = False,
                     islapsed = False,
                     nevervisible = True)

  # add weighted undirected edge to graph
  def add_undirected_edge (self, start, finish, weight = 1):
    self.G.add_edge(start, finish)
    self.G[start][finish]['weight'] = weight

  # Update visibility of node
  def check_visibility(self, index):
    n = self.G.nodes[index]
    p_protest = ((n['discontent'] 
                 * self.G.graph['efficacy']
                 * self.G.graph['homophily'])
                 + (self.get_peers_visible(index)
                 + self.G.graph['media'])/2)
                 
    threshold = ( n['threshold'] + n['burnout']) 
    if p_protest >= threshold:
      n['isvisible'] = True
      n['nevervisible'] = False
      n['islapsed'] = False
    else:
      if n['isvisible'] == True:
        n['islapsed'] = True
      n['isvisible'] = False
    #print('visibility checked')
  
  # change discontent of node
  def change_discontent(self, index, amt):
    n = self.G.nodes[index]
    # prev_viz = n['isvisible']
    n['discontent'] += amt
    self.check_visibility(index)
    # if prev_viz != n['isvisible']:
      # print(f"{index} is now visible")

  def trigger_burnout(self):
    for index in self.G.nodes:
      node = self.G.nodes[index]
      if node['isvisible']:
        node['burnout'] += .1
      else:
        node['burnout'] -= .01
  
  def duplicate(self):
    network = Network()
    network.G = self.G
    return network

  def media_reporting(self):
    amt_visible = np.mean(list(dict(self.G.nodes(data="isvisible")).values()))
    self.G.graph['media'] = amt_visible * self.G.graph['media_accuracy']
    print(self.G.graph['media'], amt_visible) 

  # Update node discontent based on surroundings
  def get_peers_visible(self, index):
    nbr_visibility = []
    for nbr_idx in self.G[index]:
      nbr = self.G.nodes[nbr_idx]
      #print(node, nx.get_node_attributes(self.G, node))
      if nbr['isvisible']:
        nbr_visibility.append(True)
      else:
        nbr_visibility.append(False)
    if len(nbr_visibility) >= 1:
      prop_nbrs_visible = np.average(nbr_visibility)
    else:
      prop_nbrs_visible = 0
    return prop_nbrs_visible

  # Simulate effect of discontent on neighbors
  def propogate_discontent(self):
    # discontent = discontent + weighted average of peers
    visible = [x for x,y in self.G.nodes(data=True) if y['isvisible']]
    for node in visible:
      # print(f"{node} is visible")
      for nbr in self.G[node]:
        # print(f'{nbr} neighbors {node}')
        self.check_visibility(nbr)
        #print(self.G.nodes[index]['discontent'])  
    self.trigger_burnout()
    self.media_reporting()

######################################

def generate_individial_stats(amt, avg_discontent, avg_threshold):
  np.random.seed(50)
  base_discontent = .3 * np.random.randn(amt) + avg_discontent
  threshold = .4 * np.random.randn(amt) + avg_threshold
  for i in range(amt):
    if base_discontent[i] > 1:
      base_discontent[i] = 1
    elif base_discontent[i] < -1:
      base_discontent[i] = -1
    if threshold[i] > 1:
      threshold[i] = 1
    elif threshold[i] < 0:
      threshold[i] = 0
  return base_discontent, threshold

def create_labels(G):
  labels = {}
  for inx, dict in G.nodes.data(): 
    labels[inx] = f"{dict['discontent']:.0f}/{dict['threshold']:.0f}"
  return labels

def create_test_nw(num_nodes = 300, avg_degree = 3, avg_discontent = .3, avg_threshold = .8):
  network = Network()
  discontent, threshold = generate_individial_stats(num_nodes, avg_discontent, avg_threshold)
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
  np.random.seed(50)
  nodes = list(network.G.nodes)
  for i in range(len(nodes) * num):
    if i == 0: 
      node1 = nodes[0]
    else:
      node1 = np.random.choice(nodes)
    node2 = np.random.choice(nodes)
    
    if node1 != node2:
      network.add_undirected_edge(node1,node2)


def run_sim(network):
  #Propogate idea
  visible = []
  lapsed = []
  networks = [network.G.copy()]

  for i in range(0,60):
    network.propogate_discontent()
    n_visible = sum(list(dict(network.G.nodes(data="isvisible")).values()))
    n_lapsed = sum(list(dict(network.G.nodes(data="islapsed")).values()))
    visible.append(n_visible)
    lapsed.append(n_lapsed)
    networks.append(network.G.copy())
  
  # Save gif
  #makeGif(networks, "contagion.gif", pos)

  # Plot contagion curve
  plt.figure()
  t = np.arange(0,len(visible),1)
  plt.stackplot(t,visible, lapsed)
  #plt.plot(t,abstain)
  plt.xlabel("Time")
  plt.ylabel("Visibly Discontent Members")
  plt.title("Discontent Contagion Curve")
  plt.show()

def main():
  print('Start')
  network = create_test_nw(500, 12, avg_threshold=.8)
  network.G.nodes[0]['isvisible'] = True
  pos = nx.kamada_kawai_layout(network.G) 
  network.G.graph['media_accuracy'] = .5

  visible = []
  lapsed = []
  networks = [network.G.copy()]

  for i in range(0,60):
    network.propogate_discontent()
    n_visible = sum(list(dict(network.G.nodes(data="isvisible")).values()))
    n_lapsed = sum(list(dict(network.G.nodes(data="islapsed")).values()))
    visible.append(n_visible)
    lapsed.append(n_lapsed)
    networks.append(network.G.copy())
  
  # Save gif
  makeGif(networks, "contagion.gif", pos)

  # Plot contagion curve
  plt.figure()
  t = np.arange(0,len(visible),1)
  plt.stackplot(t,visible, lapsed, labels= ('Visible', 'Lapsed'))
  #plt.plot(t,abstain)
  plt.xlabel("Time")
  plt.ylabel("Visibly Discontent Members")
  plt.ylim(top = 500)
  plt.title("Discontent Contagion Curve")
  plt.legend()
  plt.show()
  print("Finished")

if __name__ == "__main__":
    main()

