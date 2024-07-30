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

import networkx as nx
import numpy as np
from src.actiongraphgen.structure.node_data import NodeData


class ActionGraph:
    """This class is a representation of an action graph.

    :param max_nodes: The maximum number of nodes in the action graph.
    :type max_nodes: int

    :param param_types: A dictionary containing key-value pairs of parameter names and their types.
    :type param_types: dict
    """

    def __init__(self, max_nodes: int, param_types: dict) -> None:
        """Constructor method"""
        self.adj_matrix = np.zeros((max_nodes, max_nodes))
        self.data = NodeData(max_nodes, param_types)
        self.max_nodes = max_nodes
        self.param_types = param_types
        self.graph = self._to_graph()

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
