#  File: network_sim.py
#  Description: Initializes classes for oop approach to simulating networks
#  Code based on class code for CS 313 E

class Vertex (object):
  def __init__ (self, label, discontent, threshold):
    self.discontent = discontent
    self.threshold = threshold
    self.label = label
    self.isvisible = False

  # Check if discontent is visible to others
  def check_visibility (self):
    if self.discontent >= self.threshold:
      self.visible = True

  # determine the label of the vertex
  def get_label (self):
    return self.label

  # string representation of the vertex
  def __str__ (self):
    return str (self.label)
  
class Network (object):
  def __init__ (self):
    self.Vertices = []
    self.adjMat = []

  # check if a vertex is already in the graph
  def has_vertex (self, label):
    nVert = len (self.Vertices)
    for i in range (nVert):
      if (label == (self.Vertices[i]).get_label()):
        return True
    return False

  # given the label get the index of a vertex
  def get_index (self, label):
    nVert = len (self.Vertices)
    for i in range (nVert):
      if (label == (self.Vertices[i]).get_label()):
        return i
    return -1

  # add a Vertex with a given label to the graph
  def add_vertex (self, label, d, t):
    if (self.has_vertex (label)):
      return

    # add vertex to the list of vertices
    self.Vertices.append (Vertex(label, d, t))

    # add a new column in the adjacency matrix
    nVert = len (self.Vertices)
    for i in range (nVert - 1):
      (self.adjMat[i]).append (0)

    # add a new row for the new vertex
    new_row = []
    for i in range (nVert):
      new_row.append (0)
    self.adjMat.append (new_row)

  # add weighted undirected edge to graph
  def add_undirected_edge (self, start, finish, weight = 1):
    self.adjMat[start][finish] = weight
    self.adjMat[finish][start] = weight

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
      

def main():
    print('Start')
    network = Network()
    network.add_vertex('friend1', 5, 20)
    network.add_vertex('friend2', 10, 20)
    network.print_adj_matrix()
    network.add_undirected_edge(network.get_index('friend1',),network.get_index('friend2',))
    network.print_adj_matrix()


if __name__ == "__main__":
    main()

