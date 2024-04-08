import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from queue import Queue
import random

# Define operations
def matrix_addition(A, B):
    return np.add(A, B)

def matrix_subtraction(A, B):
    return np.subtract(A, B)

def matrix_multiplication(A, B):
    return np.matmul(A, B)

def scalar_multiplication(c, A):
    return c * A

def generate_random_matrix():
    return np.random.randint(1, 10, size=(2, 2))


# Stochastic graph generator
def generate_graph(depth):
    if depth < 1 or depth > 20:
        return None
    
    G = nx.DiGraph()
    operations = [matrix_addition, matrix_subtraction, matrix_multiplication]
    node_labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # Ensure we do not exceed the label limit
    if depth > len(node_labels) - 1:
        return None
    
    # Add root nodes with random matrices
    for i in range(depth):
        G.add_node(node_labels[i], operation=None, matrix=generate_random_matrix())
    
    # Add intermediate nodes with operations, but no matrices
    for i in range(depth, 2*depth - 1):
        G.add_node(node_labels[i], operation=random.choice(operations))
    
    # Add edges to form a valid graph
    for i in range(depth, 2*depth - 1):
        G.add_edge(node_labels[random.randint(0, i-1)], node_labels[i])
        G.add_edge(node_labels[random.randint(0, i-1)], node_labels[i])
    
    # Add terminal node
    G.add_node(node_labels[2*depth - 1], operation=random.choice(operations))
    G.add_edge(node_labels[2*depth - 2], node_labels[2*depth - 1])
    G.add_edge(node_labels[2*depth - 3], node_labels[2*depth - 1])
    
    return G

def generate_graph_2(depth):
    if depth < 1 or depth > 20:
        return None
    
    G = nx.DiGraph()
    node_labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # Ensure we do not exceed the label limit
    if depth > len(node_labels) - 1:
        return None
    
    # Add root nodes with random matrices
    for i in range(depth):
        G.add_node(node_labels[i], operation=None, matrix=generate_random_matrix())
    
    # Add intermediate nodes with operations
    for i in range(depth, 2*depth - 1):
        G.add_node(node_labels[i], operation=random.choice([0, 1, 2, 3]))
    
    # Add terminal node
    G.add_node(node_labels[2*depth - 1], operation=random.choice([0, 1, 2, 3]))
    G.add_edge(node_labels[2*depth - 2], node_labels[2*depth - 1])
    G.add_edge(node_labels[2*depth - 3], node_labels[2*depth - 1])
    
    # Generate input nodes (depth 0)
    for i in range(depth):
        G.add_node(node_labels[i], operation=None, matrix=generate_random_matrix())
    
    # Generate graph iteratively over depth 1 to d
    for k in range(1, depth):
        n = len(nx.get_node_attributes(G, 'operation')[node_labels[k-1]])
        valid_operations = random.sample(range(4), n)
        valid_operations = [op for op in valid_operations if op != 3]  # Remove scalar multiplication
        while True:
            operation = random.choice(valid_operations)
            if operation == 3:
                break
            valid_operations[valid_operations.index(operation)] = -1
        G.add_node(node_labels[k], operation=operation)
        if operation == 3:
            G.add_node(node_labels[k], scalar=random.uniform(0, 1))
        else:
            n -= 2
            while n > 0:
                parent = random.choice(node_labels[k-1])
                child = random.choice(node_labels[k-1])
                if G.has_edge(parent, child):
                    continue
                G.add_edge(parent, node_labels[k])
                G.add_edge(child, node_labels[k])
                n -= 1
    
    # Check if the graph is valid
    if not nx.is_connected(G):
        return None
    if len(nx.get_node_attributes(G, 'operation')[node_labels[2*depth - 1]]) != 1:
        return None
    if not all(nx.get_node_attributes(G, 'operation')[node_labels[i]] is None for i in range(depth)):
        return None
    if not all(nx.get_node_attributes(G, 'operation')[node_labels[i]] is not None for i in range(depth, 2*depth - 1)):
        return None
    if not all(len(nx.get_node_attributes(G, 'operation')[node_labels[i]]) == 2 for i in range(depth, 2*depth - 1)):
        return None
    if not all(nx.get_node_attributes(G, 'operation')[node_labels[i]].isdigit() for i in range(depth, 2*depth - 1)):
        return None
    return G


# Process graph in breadth-first manner
def process_graph(graph, start_node):
    queue = Queue()
    queue.put(start_node)
    visited = set()

    while not queue.empty():
        current_node = queue.get()
        if current_node not in visited:
            visited.add(current_node)
            operation = graph.nodes[current_node]['operation']
            if operation:
                # Get input matrices from predecessors
                inputs = [graph.nodes[prec]['matrix'] for prec in graph.predecessors(current_node)]
                # Apply operation and store result in current node
                if operation == scalar_multiplication:
                    c = graph.nodes[current_node]['scalar']
                    graph.nodes[current_node]['matrix'] = scalar_multiplication(c, *inputs)
                else:
                    graph.nodes[current_node]['matrix'] = operation(*inputs)
            # Add successors to the queue
            for successor in graph.successors(current_node):
                queue.put(successor)


# Iterate over each node and its attributes in the graph
def print_graph(graph):
    for node, data in graph.nodes(data=True):
        # Extract the operation and matrix result from the node's data
        operation = data.get('operation', 'No operation')  # Default to 'No operation' if not found
        matrix_result = data.get('matrix', 'No matrix')  # Default to 'No matrix' if not found
        
        # Print the node's name, operation, and matrix result
        print(f"Node: {node}")
        if callable(operation):
            print(f"Operation: {operation.__name__}")  # Get the function name if operation is callable
        else:
            print(f"Operation: {operation}")
        print(f"Matrix Result:\n{matrix_result}\n")


def main():
    depth = int(input("Enter the graph depth (1-20): "))
    while depth < 1 or depth > 20:
        print("Invalid depth. Please enter a value between 1 and 20.")
        depth = int(input("Enter the graph depth (1-20): "))
    
    G = generate_graph(depth)
    if G is None:
        print("Failed to generate a valid graph.")
        return
    
    # Process and print graph
    #process_graph(G, 'A')
    print_graph(G)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10)
    plt.show()


if __name__ == "__main__":
    main()
