import networkx as nx
import numpy as np

from node_data import NodeData


class ActionGraph:
    def __init__(self, max_nodes: int, param_types: dict) -> None:
        self.adj_matrix = np.zeros((max_nodes, max_nodes))
        self.data = NodeData(max_nodes, param_types)
        self.max_nodes = max_nodes
        self.param_types = param_types
        self.graph = self._to_graph()

    def _to_graph(self) -> nx.DiGraph:
        # Creates a networkx graph object from the adjacency matrix
        G = nx.DiGraph()
        for i in range(self.max_nodes):
            for j in range(self.max_nodes):
                if self.adj_matrix[i, j] == 1:
                    G.add_edge(i, j)
        return G
