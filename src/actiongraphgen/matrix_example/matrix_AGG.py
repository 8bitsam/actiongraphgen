##############################################################################
#
# (c) 2024 The Trustees of Columbia University in the City of New York.
# All rights reserved.
#
# File coded by: Billinge Group members and community contributors.
#
# See GitHub contributions for a more detailed list of contributors.
# https://github.com/8bitsam/actiongraphgen/graphs/contributors
#
# See LICENSE.rst for license information.
#
##############################################################################

import random

import numpy as np

from src.actiongraphgen.structure.generator import Generator


class MatrixAGG(Generator):
    """An example action graph generator (AGG) class that uses matrix operations. It extends the
    :class `actiongraphgen.structure.generator` class.

    :param max_nodes: The maximum number of nodes in the action graph.
    :type max_nodes: int

    :param: matrix: The input data for this generator. It should be a square matrix containing integers.
    :type matrix: np.ndarray
    """

    def __init__(self, max_nodes: int, matrix: np.ndarray) -> None:
        """Constructor method
        """
        param_types = {"matrix": np.ndarray, "op": int, "scalar": int}
        self.param_types = param_types
        operations = {0: "None", 1: "Inverse", 2: "Addition", 3: "Subtraction", 4: "Multiplication"}
        self.operations = operations
        super().__init__(max_nodes, param_types, operations)
        self.matrix = matrix  # terminal matrix as input to inverse problem

    def datagen(self) -> None:
        """Randomly fill in the node data for the purposes of creating random training data.
        """
        for i in range(self.max_nodes):
            # get random values and assign them to list
            scalar = random.randint(1, 100)
            op = random.randint(0, 4)
            self.action_graph.data.data_list[i]["scalar"] = scalar
            self.action_graph.data.data_list[i]["op"] = op
