import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import inv
import networkx as nx
import random

# Constants
MAX_NODES = 100
MAX_DEPTH = MAX_NODES / 10
MATRIX_SIZE = 2

# Operations dictionary
operations = {
    0: "None",
    1: "Addition",
    2: "Subtraction",
    3: "Multiplication",
    4: "Inverse"
}

# Initialize the adjacency matrix and the node details dictionary
adjacency_matrix = np.zeros((MAX_NODES, MAX_NODES), dtype=int)
node_details = {}

def generate_graph(terminal_matrix):
    # Start with the terminal node
    node_details[MAX_NODES - 1] = {'matrix': terminal_matrix, 'operation': (random.randint(0, 4), random.randint(1, 10))}
    current_node = MAX_NODES - 2  # Start generating from the second last node
    
    while current_node >= 0:
        # Randomly decide the operation for the current node
        operation, scalar = random.randint(0, 4), random.randint(1, 10)
        
        # Determine the number of parents based on the operation
        num_parents = 2 if operation in [1, 2, 3] else 1
        
        # Select parent nodes randomly from the nodes already generated
        parents = random.sample(list(range(current_node + 1, MAX_NODES)), num_parents)
        
        # Check for validity
        if is_valid_node(parents, operation):
            # Add the node to the graph
            node_details[current_node] = {'matrix': None, 'operation': (operation, scalar)}
            for parent in parents:
                adjacency_matrix[current_node, parent] = 1
            current_node -= 1

    # Create the graph object
    G = nx.DiGraph()
    for i in range(MAX_NODES):
        for j in range(MAX_NODES):
            if adjacency_matrix[i, j] == 1:
                G.add_edge(i, j)
    
    return G


def is_valid_node(parents, operation):
    """
    Implement checks based on the operation and the parents' matrices
    for validity.
    """
    
    # Check the number of parents based on the operation
    num_parents = 2 if operation in [1, 2, 3] else 1
    if len(parents) != num_parents:
        return False

    # Perform validity checks based on the operation
    if operation == 0:  # "None" operation
        return len(parents) == 1
    elif operation == 1:  # "Addition" operation
        return all(node_details[parent]['matrix'] is not None for parent in parents)
    elif operation == 2:  # "Subtraction" operation
        return all(node_details[parent]['matrix'] is not None for parent in parents)
    elif operation == 3:  # "Multiplication" operation
        return all(node_details[parent]['matrix'] is not None for parent in parents)
    elif operation == 4:  # "Inverse" operation
        return len(parents) == 1 and node_details[parents[0]]['matrix'] is not None
    else:
        return False

def visualize_graph(G):
    plt.figure(figsize=(10, 10))  # Set the figure size
    nx.draw(G, with_labels=True)
    plt.show()

    # Print out each node's details
    for node in G.nodes():
        matrix, operation = node_details[node]['matrix'], node_details[node]['operation']
        print(f"Node {node}:")
        print(f"\tMatrix: {matrix}")
        print(f"\tOperation: {operation}")
        print()

# Initialize known terminal matrix and display the graph
terminal_matrix = np.array([[1, 2], [3, 4]])
G = generate_graph(terminal_matrix)
# Print the adj matrix
print("##### ADJACENCY MATRIX #####")
print(adjacency_matrix)
print("############################")
visualize_graph(G)
