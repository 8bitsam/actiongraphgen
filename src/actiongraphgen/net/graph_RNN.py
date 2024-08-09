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

import torch
import torch.nn as nn


class GraphRNN(nn.Module):
    def __init__(self, node_feature_size, hidden_size, max_nodes):
        super(GraphRNN, self).__init__()
        self.hidden_size = hidden_size
        self.max_nodes = max_nodes

        # RNN to process node features
        self.node_rnn = nn.GRU(node_feature_size, hidden_size, batch_first=True)

        # Fully connected layers to generate adjacency matrix
        self.fc_adj = nn.Linear(hidden_size, max_nodes)

    def forward(self, node_features):
        # node_features: (batch_size, max_nodes, node_feature_size)
        batch_size = node_features.size(0)

        # Initialize hidden state
        h = torch.zeros(1, batch_size, self.hidden_size).to(node_features.device)

        # Process node features through RNN
        out, _ = self.node_rnn(node_features, h)

        # Generate adjacency matrix
        adj_logits = self.fc_adj(out) # (batch_size, max_nodes, max_nodes)

        return adj_logits
