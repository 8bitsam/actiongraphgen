==============
actiongraphgen
==============

.. image:: https://github.com/8bitsam/actiongraphgen/actions/workflows/testing.yml/badge.svg
   :target: https://github.com/8bitsam/actiongraphgen/actions/workflows/testing.yml


.. image:: https://img.shields.io/pypi/v/actiongraphgen.svg
        :target: https://pypi.python.org/pypi/actiongraphgen


A Python package containing a generative neural network that creates graphs for matrix operations called "action graphs."


* Free software: 3-clause BSD license
* Documentation: (COMING SOON!) https://8bitsam.github.io/actiongraphgen.

Features
--------
1) Generator : program that stochastiacally generates structurally valid action graphs

2) Selector : evaluates the action graphs, then scores them based on how close the terminal matrix is to the input matrix (which was the "intended" terminal matrix)

3) Database : stores the training data from the selector

4) Neural network : the actual core of the package, which is a generative AI that requires user-specified parameters.
