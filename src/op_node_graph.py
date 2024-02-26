import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from queue import Queue


# Define operations
def matrix_addition(A, B):
    return np.add(A, B)

def matrix_subtraction(A, B):
    return np.subtract(A, B)

def matrix_multiplication(A, B):
    return np.matmul(A, B)

def scalar_multiplication(c, A):
    return c * A

G = nx.DiGraph()

# Example matrices
matrix1 = np.array([[1, 2], [3, 4]])
matrix2 = np.array([[5, 6], [7, 8]])

# Add nodes with operation functions and initial matrices
G.add_node('A', operation=None, matrix=matrix1)
G.add_node('B', operation=None, matrix=matrix2)
G.add_node('C', operation=matrix_addition)
G.add_node('D', operation=matrix_multiplication)
G.add_node('E', operation=scalar_multiplication, scalar=(1/2))

# Connect nodes with edges
G.add_edge('A', 'C')
G.add_edge('B', 'C')
G.add_edge('C', 'D')
G.add_edge('A', 'D')
G.add_edge('D', 'E')

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

# Start processing from the first node
process_graph(G, 'A')

# Results
# Iterate over each node and its attributes in the graph
for node, data in G.nodes(data=True):
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

# Display graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10)
plt.show()

# Export data as json file