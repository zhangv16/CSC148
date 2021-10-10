"""Assignment 1 - Distance map (Task 1)

CSC148, Winter 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Myriam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Myriam Majedi, and Jaisie Sin.

===== Module Description =====

This module contains the class DistanceMap, which is used to store
and look up distances between cities. This class does not read distances
from the map file. (All reading from files is done in module experiment.)
Instead, it provides public methods that can be called to store and look up
distances.
"""
from typing import Dict


class DistanceMap:
    """ A map that is used to store and look up distances between cities

    === Private Attributes ===
    _map:
        A dictionary that stores the distance between cities. Each value
        represents the distance between two cities. The order of the cities
        matters.
        For example: Let <c1>, <c2> be the names of two cities, the distance
        between c1 and c2 is _map[c1c2] and the distance between c2 and c1
        is _map[c2c1].

    === Representation Invariants ===
    - _map only contains non-negative integer values。
    """
    _map: Dict[str, int]

    def __init__(self) -> None:
        self._map = {}

    def add_distance(self, c1: str, c2: str, d1: int, d2: int = None) -> None:
        """ Store the distance between <c1> and <c2> using <d1> and the distance
        between <c2> and <c1> using <d2>, if <d2> is not provided, it is by
        default set to be equal to d1.

        Precondition: <d1> and <d2> (if provided) are non-negative integers
        """
        if d2 is None:
            d2 = d1
        self._map[c1 + c2] = d1
        self._map[c2 + c1] = d2

    def distance(self, c1: str, c2: str) -> int:
        """ Return the distance between <c1> and <c2>, return -1 if the distance
        is not stored in the map
        """
        if c1 + c2 not in self._map:
            return -1
        return self._map[c1 + c2]


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
