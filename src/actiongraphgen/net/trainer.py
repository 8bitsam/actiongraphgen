#############################################################################
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
#############################################################################

import numpy as np
import torch
import torch.nn as nn


class Trainer:
    def __init__(self, data, model):
        self.data = data
        self.model = model

    def prepare_data(self):
        action_graphs = self.data
        node_features_list = []
        adj_matrices_list = []

        for graph in action_graphs:
            # Extract node parameters
            node_features = np.array([list(node_data.values()) for node_data in graph.data.data_list])
            node_features_list.append(node_features)

            # Extract adjacency matrix
            adj_matrix = graph.adj_matrix
            adj_matrices_list.append(adj_matrix)

        node_features_tensor = torch.tensor(node_features_list, dtype=torch.float32)
        adj_matrix_tensor = torch.tensor(adj_matrices_list, dtype=torch.float32)

        return node_features_tensor, adj_matrix_tensor

    def train_graph_rnn(self, node_features, adj_matrices, epochs=100, lr=0.001):
        model = self.model
        optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        criterion = nn.BCEWithLogitsLoss()

        for epoch in range(epochs):
            model.train()
            optimizer.zero_grad()

            # Forward pass
            adj_logits = model(node_features, adj_matrices)

            # Compute loss
            loss = criterion(adj_logits, adj_matrices)

            # Backward pass and optimization
            loss.backward()
            optimizer.step()

            print(f'Epoch: {epoch+1}/{epochs}, Loss: {loss.item()}')

    def generate_graph(self, initial_node_features):
        model = self.model
        model.eval()
        with torch.no_grad():
            adj_logits = model(initial_node_features)
            adj_matrix = torch.sigmoid(adj_logits).round().numpy()
        return adj_matrix
