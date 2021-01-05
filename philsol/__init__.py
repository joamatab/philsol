""" fd mode solver based on:
Full-vectorial finite-difference anaylysis of microstructured oprical fibres
Zhaoming Zhu and Thomous G Brown
"""

from philsol.core import eigen_build as eigen_build
from philsol import solve as solve
from philsol import construct as construct


__all__ = ["construct", "solve", "eigen_build"]
