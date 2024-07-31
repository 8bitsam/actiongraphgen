#!/usr/bin/env python
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

"""Structural framework for action graph generators."""

# from .database import database, drive
from .matrix_example import matrix_AGG
from .structure import action_graph, generator, node_data
from .version import __version__

__all__ = ['matrix_AGG', 'action_graph', 'generator', 'node_data', '__version__']

# silence the pyflakes syntax checker
assert __version__ or True

# End of file
