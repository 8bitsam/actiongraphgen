from src.actiongraphgen.structure.generator import Generator
import numpy as np
import random


class MatrixAGG(Generator):
    def __init__(self, max_nodes: int, matrix: np.ndarray) -> None:
        param_types = {"matrix": np.ndarray, "op": int, "scalar": int}
        self.param_types = param_types
        operations = {0: "None", 1: "Inverse", 2: "Addition", 3: "Subtraction", 4: "Multiplication"}
        self.operations = operations
        super().__init__(max_nodes, param_types, operations)
        self.matrix = matrix  # terminal matrix as input to inverse problem

    def datagen(self) -> None:
        for i in range(self.max_nodes):
            # get random values and assign them to list
            scalar = random.randint(1, 100)
            op = random.randint(0, 4)
            self.action_graph.data.data_list[i]["scalar"] = scalar
            self.action_graph.data.data_list[i]["op"] = op
