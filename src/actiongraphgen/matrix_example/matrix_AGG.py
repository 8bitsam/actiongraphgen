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

    def datagen(self) -> None:
        """Randomly fill in the node data for the purposes of creating random training data."""
        adj_matrix = self.action_graph.adj_matrix

        for i in range(self.max_nodes):
            # 1's in row i represent children -> find 1's for this
            # 1's in column i represent parents -> add 1's for this

            # get random values and assign them to list
            scalar = random.randint(1, 100)
            op = random.randint(0, 4)

            # evaluate based on operation
            child_pos = self.action_graph.get_child_nodes(i)[0]  # nodes in this action graph only ever have one child

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

            # add parent positions
            # start case
            if i == 0:
                self.action_graph.data.data_list[i]["matrix"] = self.matrix
                continue
            # non-start case
            if one_parent:
                parent_pos.append(i + 1)
                adj_matrix[:, i][i] = 1
            elif two_parents:
                parent_pos.extend([i + 1, i + 2])
            self.action_graph.fill_parents(i, parent_pos)

            # add parent matrix data
            # select helper based on op
            match op:
                case 0: self.action_graph.data.data_list[i]["matrix"] = self._datagen_none(parent_pos)
                case 1: self.action_graph.data.data_list[i]["matrix"] = self._datagen_inv(parent_pos)
                case 2: self.action_graph.data.data_list[i]["matrix"] = self._datagen_inv(parent_pos)
                case 3: self.action_graph.data.data_list[i]["matrix"] = self._datagen_inv(parent_pos)
                case 4: self.action_graph.data.data_list[i]["matrix"] = self._datagen_inv(parent_pos)

    def _datagen_none(self, children: list[int]) -> np.ndarray:
        """Protected helper method for datagen; for the "None" operation.
        Returns the calculated matrix.
        :param children: List of the indices of the child nodes.
        :type children: list

        :rtype: np.ndarray
        """
        pos = children[0]
        scalar = self.action_graph.data.data_list[pos]["scalar"]
        matrix = self.action_graph.data.data_list[pos]["matrix"]
        matrix = matrix / scalar
        return matrix

    def _datagen_inv(self, children: list[int]) -> np.ndarray:
        """Protected helper method for datagen; for the "Inverse" operation.
                Returns the calculated matrix.
        :param children: List of the indices of the child nodes.
        :type children: list

        :rtype: np.ndarray
        """
        pos = children[0]
        scalar = self.action_graph.data.data_list[pos]["scalar"]
        matrix = self.action_graph.data.data_list[pos]["matrix"]
        matrix = matrix / scalar
        matrix = np.invert(matrix)
        return matrix

    def _datagen_add(self, children: list[int]) -> np.ndarray:
        """Protected helper method for datagen; for the "Addition" operation.
                Returns the calculated matrix.
        :param children: List of the indices of the child nodes.
        :type children: list

        :rtype: np.ndarray
        """
        pos = children[0]
        scalar = self.action_graph.data.data_list[pos]["scalar"]
        matrix = self.action_graph.data.data_list[pos]["matrix"]
        matrix = matrix / scalar
        # TODO: finish add operation
        return matrix

    def _datagen_sub(self, children: list[int]) -> np.ndarray:
        """Protected helper method for datagen; for the "Subtraction" operation.
                Returns the calculated matrix.
        :param children: List of the indices of the child nodes.
        :type children: list

        :rtype: np.ndarray
        """
        pos = children[0]
        scalar = self.action_graph.data.data_list[pos]["scalar"]
        matrix = self.action_graph.data.data_list[pos]["matrix"]
        matrix = matrix / scalar
        # TODO: finish sub operation
        return matrix

    def _datagen_mul(self, children: list[int]) -> np.ndarray:
        """Protected helper method for datagen; for the "Multiplication" operation.
                Returns the calculated matrix.
        :param children: List of the indices of the child nodes.
        :type children: list

        :rtype: np.ndarray
        """
        pos = children[0]
        scalar = self.action_graph.data.data_list[pos]["scalar"]
        matrix = self.action_graph.data.data_list[pos]["matrix"]
        matrix = matrix / scalar
        # TODO: finish mul operation
        return matrix


# testing (remove later)
if __name__ == "__main__":
    A = np.array([[1, 2], [3, 4]])
    tester = MatrixAGG(max_nodes=10, matrix=A)
    tester.datagen()
    print(tester.action_graph.data.data_list)
