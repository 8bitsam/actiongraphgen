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
        """Constructor method"""
        param_types = {"matrix": np.ndarray, "op": int, "scalar": int}
        self.param_types = param_types
        operations = {0: "None", 1: "Inverse", 2: "Addition", 3: "Subtraction", 4: "Multiplication"}
        self.operations = operations
        super().__init__(max_nodes, param_types, operations)
        self.matrix = matrix  # terminal matrix as input to inverse problem
        self.action_graph.data.data_list[0]["matrix"] = self.matrix

    def _datagen_none(self, pos: int) -> np.ndarray:
        """Protected helper method for datagen; for the "None" operation.
        Returns the calculated matrix.

        :param pos: The index of a node in the adjacency matrix.
        :type pos: int

        :rtype: np.ndarray
        """
        scalar = self.action_graph.data.data_list[pos]["scalar"]
        matrix = self.action_graph.data.data_list[pos]["matrix"]
        matrix = matrix / scalar
        return matrix

    def _datagen_inv(self, pos: int) -> np.ndarray:
        """Protected helper method for datagen; for the "Inverse" operation.
                Returns the calculated matrix.

        :param pos: The index of a node in the adjacency matrix.
        :type pos: int

        :rtype: np.ndarray
        """
        scalar = self.action_graph.data.data_list[pos]["scalar"]
        matrix = self.action_graph.data.data_list[pos]["matrix"]
        matrix = matrix / scalar
        matrix = np.linalg.inv(matrix)
        return matrix

    def _datagen_add(self, pos: int) -> np.ndarray:
        """Protected helper method for datagen; for the "Addition" operation.
        Returns the calculated matrices for both parents.

        :param pos: The index of a node in the adjacency matrix.
        :type pos: int

        :rtype: np.ndarray
        """
        scalar = self.action_graph.data.data_list[pos]["scalar"]
        matrix = self.action_graph.data.data_list[pos]["matrix"]
        matrix = matrix / scalar
        n = len(self.matrix[0])
        # matrix/scalar = A + B
        if random.randint(0, 1) == 0:
            A = np.random.randint(1, 11, size=(n, n))
            B = matrix - A
        else:
            B = np.random.randint(1, 11, size=(n, n))
            A = matrix - B
        return np.array([A, B])

    def _datagen_sub(self, pos: int) -> np.ndarray:
        """Protected helper method for datagen; for the "Subtraction" operation.
        Returns the calculated matrices for both parents.

        :param pos: The index of a node in the adjacency matrix.
        :type pos: int

        :rtype: np.ndarray
        """
        scalar = self.action_graph.data.data_list[pos]["scalar"]
        matrix = self.action_graph.data.data_list[pos]["matrix"]
        matrix = matrix / scalar
        n = len(self.matrix[0])
        # matrix/scalar = A - B
        if random.randint(0, 1) == 0:
            A = np.random.randint(1, 11, size=(n, n))
            B = A - matrix
        else:
            B = np.random.randint(1, 11, size=(n, n))
            A = matrix + B
        return np.array([A, B])

    def _datagen_mul(self, pos: int) -> np.ndarray:
        """Protected helper method for datagen; for the "Multiplication" operation.
        Returns the calculated matrices for both parents.

        :param pos: The index of a node in the adjacency matrix.
        :type pos: int

        :rtype: np.ndarray
        """
        scalar = self.action_graph.data.data_list[pos]["scalar"]
        matrix = self.action_graph.data.data_list[pos]["matrix"]
        matrix = matrix / scalar
        n = len(self.matrix[0])
        A = np.random.randint(1, 11, size=(n, n))
        B = np.ones((n, n))
        for i in range(0, n):
            for j in range(0, n):
                B[i][j] = matrix[i][j] / A[i][j]
        return np.array([A, B])

    def datagen(self) -> None:
        """Randomly fill in the node data for the purposes of creating random training data."""
        adj_matrix = self.action_graph.adj_matrix

        for i in range(self.max_nodes):
            # get random values and assign them to list
            scalar = random.randint(1, 100)
            op = random.randint(0, 4)

            # error catching
            # exclude "Inverse" operation if the matrix is singular
            if np.linalg.det(self.action_graph.data.data_list[i]["matrix"]) == 0 and op == 1:
                op = random.choice([0, 2, 3, 4])

            # choose positions for parents
            parent_pos = []
            one_parent = op == 0 or op == 1
            two_parents = op == 2 or op == 3 or op == 4

            # termination condition for root nodes
            if (one_parent and (self.max_nodes - i) <= 1) or (two_parents and (self.max_nodes - i) <= 2):
                break

            # if not terminated can set values
            self.action_graph.data.data_list[i]["scalar"] = scalar
            self.action_graph.data.data_list[i]["op"] = op

            # generate parent nodes
            parent_pos.append(i + 1)
            if two_parents:
                parent_pos.append(i + 2)
            for parent in parent_pos:
                adj_matrix[:, i][parent] = 1
            self.action_graph.fill_parents(i, parent_pos)

            # add parent matrix data
            # select helper based on op
            match op:
                case 0:
                    matrix = self._datagen_none(i)
                    self.action_graph.data.data_list[parent_pos[0]]["matrix"] = matrix
                case 1:
                    matrix = self._datagen_inv(i)
                    self.action_graph.data.data_list[parent_pos[0]]["matrix"] = matrix
                case 2:
                    matrices = self._datagen_add(i)
                    self.action_graph.data.data_list[parent_pos[0]]["matrix"] = matrices[0]
                    self.action_graph.data.data_list[parent_pos[1]]["matrix"] = matrices[1]
                case 3:
                    matrices = self._datagen_sub(i)
                    self.action_graph.data.data_list[parent_pos[0]]["matrix"] = matrices[0]
                    self.action_graph.data.data_list[parent_pos[1]]["matrix"] = matrices[1]
                case 4:
                    matrices = self._datagen_mul(i)
                    if np.random.randint(0, 1) == 0:
                        self.action_graph.data.data_list[parent_pos[0]]["matrix"] = matrices[0]
                        self.action_graph.data.data_list[parent_pos[1]]["matrix"] = matrices[1]
                    else:
                        self.action_graph.data.data_list[parent_pos[1]]["matrix"] = matrices[0]
                        self.action_graph.data.data_list[parent_pos[0]]["matrix"] = matrices[1]

        # update nx graph object
        self.action_graph.update_graph()
