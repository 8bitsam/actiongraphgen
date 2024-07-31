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

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from actiongraphgen.structure.node_data import NodeData


class ActionGraph:
    """This class is a representation of an action graph.

    :param max_nodes: The maximum number of nodes in the action graph.
    :type max_nodes: int

    :param param_types: A dictionary containing key-value pairs of parameter names and their types.
    :type param_types: dict
    """

    def _to_graph(self) -> nx.DiGraph:
        """Protected method that creates a networkx DiGraph object from the adjacency matrix.

        :rtype: nx.DiGraph
        """
        G = nx.DiGraph()
        for i in range(self.max_nodes):
            for j in range(self.max_nodes):
                if self.adj_matrix[i, j] == 1:
                    G.add_edge(i, j)
        return G

    def __init__(self, max_nodes: int, param_types: dict) -> None:
        """Constructor method"""
        self.adj_matrix = np.zeros((max_nodes, max_nodes))
        self.data = NodeData(max_nodes, param_types)
        self.max_nodes = max_nodes
        self.param_types = param_types
        self.graph = self._to_graph()

    def display(self) -> None:
        """Display the graph using matplotlib."""
        pos = nx.spring_layout(self.graph, k=2 / np.sqrt(self.graph.order()), iterations=50)
        nx.draw(self.graph, pos, with_labels=True, node_size=500, arrowsize=20)
        plt.title("Directed Graph")
        plt.axis("off")
        plt.show()

    def fill_parents(self, node_pos: int, parents: list[int]) -> None:
        """Fill in the adjacency matrix to denote parent positions.
        :param node_pos: The index of the node, which is in range [0, max_nodes), to fill in the parents of.
        :type node_pos: int

        :param parents: A list of indices of the node's parents, also in range [0, max_nodes).
        :type parents: list[int]
        """
        adj_matrix = self.adj_matrix
        for parent in parents:
            col = adj_matrix[:, node_pos]
            col[parent] = 1

    def get_children(self, node: int) -> np.ndarray:
        """Get all the positions of a node's children and return them in an array.
        :param node: The index of the node (within the adjacency matrix) to find child positions for.
        :type node: int

        :rtype: np.ndarray
        """
        row = self.adj_matrix[node]
        return np.nonzero(row)[0]

    def get_parents(self, node: int):
        """Get all the positions of a node's parents and return them in an array.
        :param node: The index of the node (within the adjacency matrix) to find parent positions for.
        :type node: int

        :rtype: np.ndarray
        """
        col = self.adj_matrix[:, node]
        return np.nonzero(col)[0]

    def update_graph(self) -> None:
        """Update the networkx DiGraph object according to current data."""
        self.graph = self._to_graph()
