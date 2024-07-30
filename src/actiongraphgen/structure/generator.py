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

from src.actiongraphgen.structure.action_graph import ActionGraph


class Generator:
    """A small class to represent the structure of a general action graph generator. It
    contains the structure and [TODO: add additional required components like neural net, etc].
    See the :class:`actiongraphen.matrix_example.matrix_AGG` class for example usage.

    :param max_nodes: The maximum number of nodes in the action graph.
    :type max_nodes: int

    :param param_types: A dictionary containing key-value pairs of parameter names and their types.
    :type param_types: dict

    :param processes: A dictionary containing key-value pairs of process names and their type mappings.
    :type processes: dict
    """

    def __init__(self, max_nodes: int, param_types: dict, processes: dict) -> None:
        """Constructor method"""
        self.max_nodes = max_nodes
        self.param_types = param_types
        self.processes = processes
        self.action_graph = ActionGraph(max_nodes, param_types)
