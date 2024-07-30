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

class NodeData:
    """This class represents a data object that contains node data and storage parameters for the action graph.

    :param max_nodes: The maximum number of nodes in the action graph.
    :type max_nodes: int

    :param param_types: A dictionary containing key-value pairs of parameter names and their types.
    :type param_types: dict
    """

    def __init__(self, max_nodes: int, param_types: dict) -> None:
        """Constructor method
        """
        self.max_nodes = max_nodes
        self.param_types = param_types
        self.data_list = self._init_data()

    def _init_data(self) -> list[dict]:
        """Protected method that initializes a node parameter dictionary list filled
        with None type objects.

        :rtype: list[dict]
        """
        lst = []
        for _ in range(self.max_nodes):
            data_dict = {param: None for param, dtype in self.param_types.items()}
            lst.append(data_dict)
        return lst
