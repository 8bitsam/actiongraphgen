from action_graph import ActionGraph
from generator import Generator
import matplotlib.pyplot as plt
import networkx as nx
from node_data import NodeData
import numpy as np
import random


class MatrixAGG(Generator):
    def __init__(self, max_nodes : int) -> None:
        param_types = {
            "matrix" : np.ndarray,
            "op" : int,
            "scalar" : int
        }
        self.param_types = param_types
        operations = {
            0 : "None",
            1 : "Inverse",
            2 : "Addition",
            3 : "Subtraction",
            4 : "Multiplication"
        }
        self.operations = operations
        super().__init__(max_nodes, param_types, operations)