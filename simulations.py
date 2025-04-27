import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from matplotlib.animation import FuncAnimation, PillowWriter
import tempfile
import base64
import os

# ------------------------
# Simulation Core
# ------------------------

class Network:
    def __init__(self):
        self.G = nx.Graph()

    def add_node(self, d, t):
        index = len(self.G.nodes)
        self.G.add_node(index, discontent=d, threshold=t, isvisible=False)
        self.check_visibility(index)

    def check_visibility(self, index):
        node = self.G.nodes[index]
        node['isvisible'] = node['discontent'] >= node['threshold']

    def change_discontent(self, index, amt):
        node = self.G.nodes[index]
        node['discontent'] += amt
        self.check_visibility(index)

    def add_undirected_edge(self, a, b, weight=1):
        self.G.add_edge(a, b, weight=weight)

    def observe_discontent(self, index):
        peer_discontent = [
            self.G.nodes[n]['discontent'] * self.G[index][n]['weight']
            for n in self.G[index]
            if self.G.nodes[n]['isvisible']
        ]
        if peer_discontent:
            avg_discontent = np.mean(peer_discontent)
            self.change_discontent(index, avg_discontent)

    def propogate_discontent(self):
        visible = [n for n, attr in self.G.nodes(data=True) if attr['isvisible']]
        for node in visible:
            for neighbor in self.G[node]:
                self.observe_discontent(neighbor)

def generate_individial_stats(n):
    discontent = 10 * np.random.randn(n) + 5
    threshold = 10 * np.random.randn(n) + 30
    return discontent, threshold

def create_connections(network, degree):
    nodes = list(network.G.nodes)
    for _ in range(len(nodes) * degree):
        a, b = np.random.choice(nodes, 2, replace=False)
        if a != b:
            network.add_undirected_edge(a, b)

def create_test_nw(n, degree):
    net = Network()
    discontent, threshold = generate_individial_stats(n)
    for d, t in zip(discontent, threshold):
        net.add_node(d, t)
    create_connections(net, degree)
    return net

def get_color(G):
    return ["red" if G.nodes[n]['isvisible'] else "blue" for n in G.nodes]

# ------------------------
# Animation Function
# ------------------------

def render_animation(networks, pos):
    fig, ax = plt.subplots(figsize=(6, 6))

    def update(i):
        ax.clear()
        nx.draw(networks[i], pos=pos, node_color=get_color(networks[i]), ax=ax, with_labels=False)
        ax.set_title(f"Step {i}")

    ani = FuncAnimation(fig, update, frames=len(networks), interval=500)

    # Save GIF to temporary file
    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmpfile:
        gif_path = tmpfile.name
    ani.save(gif_path, writer=PillowWriter(fps=2))
    plt.close(fig)

    # Read GIF and encode as base64 for embedding
    with open(gif_path, "rb") as f:
        gif_data = f.read()
    os.remove(gif_path)

    b64 = base64.b64encode(gif_data).decode()
    html = f'<img src="data:image/gif;base64,{b64}" width="100%" />'
    return html

# ------------------------
# Streamlit App UI
# ------------------------

st.set_page_config(page_title="Network Simulation", layout="centered")
st.title("📊 Network Contagion Simulation")
st.markdown("Visualize how discontent spreads across a social network.")

num_nodes = st.slider("🔢 Number of Nodes", 10, 200, 100)
avg_degree = st.slider("🔗 Average Degree per Node", 1, 10, 3)
iterations = st.slider("⏱️ Propagation Steps", 1, 100, 50)

if st.button("Run Simulation"):
    st.info("Running simulation...")
    network = create_test_nw(num_nodes, avg_degree)
    pos = nx.kamada_kawai_layout(network.G)

    snapshots = [network.G.copy()]
    for _ in range(iterations):
        network.propogate_discontent()
        snapshots.append(network.G.copy())

    # Track visible nodes over time
    visible_counts = [
        sum(1 for _, attr in G.nodes(data=True) if attr["isvisible"])
        for G in snapshots
    ]

    # Show GIF
    html = render_animation(snapshots, pos)
    st.components.v1.html(html, height=600)

    # Show static graphs
    st.subheader("🔍 Initial Network State")
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    nx.draw(snapshots[0], pos=pos, node_color=get_color(snapshots[0]), ax=ax1, with_labels=False)
    st.pyplot(fig1)

    st.subheader("📌 Final Network State")
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    nx.draw(snapshots[-1], pos=pos, node_color=get_color(snapshots[-1]), ax=ax2, with_labels=False)
    st.pyplot(fig2)

    # Show line graph of visible node count
    st.subheader("📈 Discontent Spread Over Time")
    fig3, ax3 = plt.subplots()
    ax3.plot(range(len(visible_counts)), visible_counts, marker='o')
    ax3.set_xlabel("Step")
    ax3.set_ylabel("Visible Nodes")
    ax3.set_title("Number of Visible Nodes at Each Step")
    st.pyplot(fig3)

    st.success("Simulation complete!")
