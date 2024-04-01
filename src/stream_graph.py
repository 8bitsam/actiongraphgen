import numpy as np
from streamz import Stream

# Define operations
def matrix_addition(A, B):
    return np.add(A, B)

def matrix_multiplication(A, B):
    return np.matmul(A, B)

# Create a node that performs an operation on input from other nodes
def create_operation_node(operation_func, *input_streams):
    node = Stream()
    node.map(operation_func, *input_streams)
    return node

# Define input matrices A and B
matrix_a = np.array([[1, 2], [3, 4]])
matrix_b = np.array([[5, 6], [7, 8]])

# Create nodes for operations
add_node = create_operation_node(matrix_addition)
mul_node = create_operation_node(matrix_multiplication)

# Define the graph structure with nodes C and D
graph = {
    'add': (add_node, ['input_a', 'input_b'], 'C'),  # Node C for addition result
    'mul': (mul_node, ['C', 'input_a'], 'D')          # Node D for multiplication result
}

# Example of setting up input streams
input_stream_a = Stream()
input_stream_b = Stream()

# Connect input streams to the graph
graph['add'][0].connect(input_stream_a)
graph['add'][0].connect(input_stream_b)

# Print and execute
def print_step(operation, result):
    print(f"Operation: {operation.__name__}, Result: \n{result}")

results = {}  # Dictionary to store results at each step

# Attach print_step function to each operation node and store results
for key, (node, _, result_key) in graph.items():
    for upstream_node in node.upstreams:
        upstream_node.sink(lambda x, key=result_key: results.update({key: x}), operation=node.map)
        node.sink(print_step, operation=node.map)

print("Initial Matrices:")
print("Matrix A:\n", matrix_a)
print("Matrix B:\n", matrix_b)

input_stream_a.emit(matrix_a)
input_stream_b.emit(matrix_b)

# Print final result from node D (node 'mul')
final_result = results.get('D', None)  # Access result from 'D' node
if final_result is not None:
    print("\nFinal Result (Node D):")
    print(final_result[-1])  # Retrieve the last result from the list of results for 'D'
else:
    print("\nFinal Result (Node D) not available. Check your graph structure.")

print(results)
