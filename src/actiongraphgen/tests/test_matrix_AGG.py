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

import random

import numpy as np

from actiongraphgen.matrix_example.matrix_AGG import MatrixAGG


def test_datagen():
    n = random.randint(2, 5)
    A = np.random.randint(low=1, high=10, size=(n, n))
    tester = MatrixAGG(max_nodes=random.randint(5, 100), matrix=A)

    try:
        tester.datagen()
        assert True
    except Exception:
        assert False, "matrix_AGG.datagen() raised an exception."


if __name__ == "__main__":
    # Do 10 runs
    for i in range(10):
        test_datagen()
