"""Assignment 1 - Scheduling algorithms (Task 4)

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

This module contains the abstract Scheduler class, as well as the two
subclasses RandomScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.
"""
from typing import List, Dict, Callable
from random import shuffle, choice
from container import PriorityQueue
from domain import Parcel, Truck


class Scheduler:
    """A scheduler, capable of deciding what parcels go onto which trucks, and
    what route each truck will take.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks>, that is, decide
        which parcels will go on which trucks, as well as the route each truck
        will take.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what route they will
        take.  Do *not* mutate the list <parcels>, or any of the parcel objects
        in that list.

        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        raise NotImplementedError


class RandomScheduler(Scheduler):
    """ The randomized implementation of the Scheduler class"""
    def __init__(self) -> None:
        return

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """ Schedule packing using randomized algorithm. """
        ps = parcels[:]
        shuffle(ps)
        non_packed = []
        for p in ps:
            ts = []
            for truck in trucks:
                if truck.get_available_capacity() >= p.volume:
                    ts.append(truck)
            if len(ts) > 0:
                choice(ts).pack(p)
            else:
                non_packed.append(p)
        return non_packed


class GreedyScheduler(Scheduler):
    """ The greedy implementation of Scheduler class
    === Private Attributes ===
    _parcel_priority:
        The way which the priority of parcels is determined
    _parcel_order:
        The order that parcels will be processed
    _truck_order:
        The order which trucks will be picked for packing parcels

    === Representation Invariants ===
    - _parcel_priority is either 'volume' or 'destination'
    - _parcel_order is either 'non-decreasing' or 'non-increasing'
    - _truck_order is either 'non-decreasing' or 'non-increasing'
    """
    _parcel_priority: str
    _parcel_order: str
    _truck_order: str

    def __init__(self, config: Dict[str, str]) -> None:
        """ Initialize the scheduler with the given configuration

        Precondition: <config> contains keys and values as specified
        in Assignment 1.
        """

        self._parcel_priority = config["parcel_priority"]
        self._parcel_order = config["parcel_order"]
        self._truck_order = config["truck_order"]

    def _compare_func_parcel(self) -> Callable[[Parcel, Parcel], bool]:
        """ Determine which comparing function to use on parcels with regards to
         the configuration.
        """
        if self._parcel_priority == 'volume':
            if self._parcel_order == 'non-decreasing':
                return _compare_parcel_volume_ndc
            return _compare_parcel_volume_nic
        if self._parcel_order == 'non-decreasing':
            return _compare_parcel_destination_ndc
        return _compare_parcel_destination_nic

    def _compare_func_truck(self) -> Callable[[Truck, Truck], bool]:
        """ Determine which comparing function to use on trucks with regards to
         the configuration.
        """
        if self._truck_order == 'non-decreasing':
            return _compare_truck_freespace_ndc
        return _compare_truck_freespace_nic

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """ Schedule packing using greedy algorithm """
        comp1 = self._compare_func_parcel()
        ps = PriorityQueue(comp1)
        unpacked = []
        for p in parcels:
            ps.add(p)
        while not ps.is_empty():
            p = ps.remove()
            temp = []
            temp2 = []
            comp2 = self._compare_func_truck()
            ts = PriorityQueue(comp2)
            for t in trucks:
                if t.get_available_capacity() >= p.volume:
                    temp.append(t)
            for t in temp:
                if len(t.route) > 0 and t.route[-1] == p.destination:
                    temp2.append(t)
            if len(temp2) > 0:
                temp = temp2
            for t in temp:
                ts.add(t)
            if len(temp) > 0:
                t = ts.remove()
                t.pack(p)
            else:
                unpacked.append(p)
        return unpacked


def _compare_parcel_volume_ndc(p1: Parcel, p2: Parcel) -> bool:
    """ Compare parcels by their volume in non-decreasing order """
    return p1.volume < p2.volume


def _compare_parcel_volume_nic(p1: Parcel, p2: Parcel) -> bool:
    """ Compare parcels by their volume in non-increasing order """
    return p1.volume > p2.volume


def _compare_parcel_destination_ndc(p1: Parcel, p2: Parcel) -> bool:
    """ Compare parcels by their destination in non-decreasing order """
    return p1.destination < p2.destination


def _compare_parcel_destination_nic(p1: Parcel, p2: Parcel) -> bool:
    """ Compare parcels by their destination in non-increasing order """
    return p1.destination > p2.destination


def _compare_truck_freespace_ndc(t1: Truck, t2: Truck) -> bool:
    """ Compare trucks by their free capacity in non-decreasing order """
    return t1.get_available_capacity() < t2.get_available_capacity()


def _compare_truck_freespace_nic(t1: Truck, t2: Truck) -> bool:
    """ Compare trucks by their free capacity in non-increasing order """
    return t1.get_available_capacity() > t2.get_available_capacity()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['compare_algorithms'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', 'container', 'domain'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
