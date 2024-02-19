import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


# Map for operations
str_to_op = {
    "scalar multiplication" : 0,
    "addition" : 1,
    "multiplication" : 2
}

op_to_str = { # this is just for printing
    0 : "scalar multiplication",
    1 : "addition",
    2 : "multiplication"
}

# Function to do operation based on edge weight
func_map = {
    0 : lambda x, c: x*c,
    1 : lambda x, y: x + y,
    2 : lambda x, y: np.multiply(x, y)
}

# Initial state
G = nx.Graph()
G.add_node('A', matrix=np.array([[1, 2], [3, 4]]))
G.add_node('B', matrix=np.array([[0, 0], [0, 0]]))
G.add_edge('A', 'B', weight=str_to_op['scalar multiplication'])

# Perform operation
M = G.nodes['A']['matrix']
op = G.get_edge_data('A', 'B')['weight']
N = func_map[op](M, 2)
G.nodes['B']['matrix'] = N

# Return state and display graph
print("Initial matrix: ", M)
print("Operation: ", op_to_str[op])
print("Final matrix: ", N)
pos= nx.spring_layout(G)
nx.draw_networkx(G, pos)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()