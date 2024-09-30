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

import pytest

from actiongraphgen.structure.action_graph import ActionGraph

from .math_action_graph import MathNodeData


@pytest.fixture
def math_graph():
    """Create a math action graph for testing."""
    param_types = {"operation": str, "amount": float, "factor": float}
    graph = ActionGraph(3, param_types, node_data_class=MathNodeData)

    # Manually set up a simple DAG: node 0 -> node 1 -> node 2
    graph.fill_parents(1, [0])  # node 1 depends on node 0
    graph.fill_parents(2, [1])  # node 2 depends on node 1

    # Set operations for each node
    graph.data.data_list[0]["operation"] = "add"
    graph.data.data_list[0]["amount"] = 10

    graph.data.data_list[1]["operation"] = "multiply"
    graph.data.data_list[1]["factor"] = 2

    return graph


@pytest.mark.asyncio
async def test_math_graph_processing(math_graph):
    """Test processing a data stream through the math action graph."""
    input_stream = [5, 10, 20]

    # Expected processing:
    # Input 5: (5 + 10) * 2 = 30
    # Input 10: (10 + 10) * 2 = 40
    # Input 20: (20 + 10) * 2 = 60
    expected = [30, 40, 60]

    result = math_graph.process_stream(input_stream)

    assert result == expected, f"Expected {expected} but got {result}"
