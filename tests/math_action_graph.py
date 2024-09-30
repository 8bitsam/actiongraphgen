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

from actiongraphgen.structure.node_data import NodeData


def _process_add(input_data: float, node_params: dict) -> float:
    """Add a specified amount to the input data."""
    amount = node_params.get("amount", 0)
    return input_data + amount


def _process_multiply(input_data: float, node_params: dict) -> float:
    """Multiply the input data by a specified factor."""
    factor = node_params.get("factor", 1)
    return input_data * factor


class MathNodeData(NodeData):
    """A subclass of NodeData for performing basic math operations on nodes."""

    def process_node(self, node_pos: int, input_data: float) -> float:
        """Process input data by performing basic math operations.
        Node parameters must include 'operation' (e.g., 'add', 'multiply') and relevant values.
        """
        node_params = self.data_list[node_pos]
        operation = node_params.get("operation")

        if operation == "add":
            return _process_add(input_data, node_params)
        elif operation == "multiply":
            return _process_multiply(input_data, node_params)
        else:
            return input_data
