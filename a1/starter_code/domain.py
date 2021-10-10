"""Assignment 1 - Domain classes (Task 2)

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

This module contains the classes required to represent the entities
in the simulation: Parcel, Truck and Fleet.
"""
from typing import List, Dict
from distance_map import DistanceMap


class Parcel:
    """ A parcel that awaits delivery to its destination

    === Public Attributes ===
    source:
        The city where the parcel came from.
    destination:
        The city where the parcel will be delivered.
    volume:
        The volume of the parcel, measured in cc.
    id:
        The id of the parcel.

    === Representation Invariants ===
    - volume > 0
    """
    source: str
    destination: str
    volume: int
    id: int

    # It must be consistent with the Fleet class docstring examples below.
    def __init__(self, i: int, vol: int, c1: str, c2: str) -> None:
        """ Initialize a new parcel with the information provided, where i is
        the id of the parcel, vol is the volume of the parcel, measured in cc,
        c1 is the source of the parcel, c2 is the destination of the parcel.

        Precondition: vol > 0
        """
        self.id = i
        self.volume = vol
        self.source = c1
        self.destination = c2


class Truck:
    # It must be consistent with the Fleet class docstring examples below.
    """ A truck that delivers parcels to their destinations

    === Public Attributes ===
    capacity:
        The volume capacity of the truck, measured in cc.
    id:
        The id of the truck.
    route:
        List of the city names this truck will go through.
    depot:
        The depot of the truck.
    parcels:
        The parcels this truck carries

    === Representation Invariants ===
    - capacity > 0
    - The sum of the volume of the parcels this truck carries must not exceed
    its capacity.
    """
    capacity: int
    parcels: List[Parcel]
    id: int
    route: List[str]
    depot: str

    def __init__(self, i: int, cap: int, dep: str) -> None:
        """ Initialize the truck with the provided information, where i is the
        id of the truck, cap is the capacity of the truck, and dep is the depot
        of the truck.

        Precondition: cap > 0
        """
        self.id = i
        self.capacity = cap
        self.depot = dep
        self.route = []
        self.parcels = []

    def pack(self, p: Parcel) -> bool:
        """ Pack the parcel onto the truck if there's enough space and no parcel
        with the same id is onboard.
        Return True if successfully packed, return False otherwise.
        """
        for pr in self.parcels:
            if pr.id == p.id:
                return False
        if self.get_available_capacity() - p.volume < 0:
            return False
        self.parcels.append(p)
        self.route.append(p.destination)
        return True

    def get_available_capacity(self) -> int:
        """ Return the available capacity """
        total_vol = 0
        for p in self.parcels:
            total_vol += p.volume
        return self.capacity - total_vol

    def fullness(self) -> float:
        """ Return the fullness of the truck in percentage. """
        num = self.get_available_capacity() / self.capacity
        return 100 - num * 100


class Fleet:
    """ A fleet of trucks for making deliveries.

    ===== Public Attributes =====
    trucks:
      List of all Truck objects in this fleet.
    """
    trucks: List[Truck]

    def __init__(self) -> None:
        """Create a Fleet with no trucks.

        >>> f = Fleet()
        >>> f.num_trucks()
        0
        """

        self.trucks = []

    def add_truck(self, truck: Truck) -> None:
        """Add <truck> to this fleet.

        Precondition: No truck with the same ID as <truck> has already been
        added to this Fleet.

        >>> f = Fleet()
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> f.add_truck(t)
        >>> f.num_trucks()
        1
        """
        for t in self.trucks:
            if t.id == truck.id:
                return
        self.trucks.append(truck)

    # We will not test the format of the string that you return -- it is up
    # to you.
    def __str__(self) -> str:
        """Produce a string representation of this fleet
        """
        result = []
        for i in self.trucks:
            result.append(str(i.id) + ' ' + '->' + ' ')
        return str(result)

    def num_trucks(self) -> int:
        """Return the number of trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> f.num_trucks()
        1
        """
        return len(self.trucks)

    def num_nonempty_trucks(self) -> int:
        """Return the number of non-empty trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        True
        >>> t1.fullness()
        90.0
        >>> t2 = Truck(5912, 20, 'Toronto')
        >>> f.add_truck(t2)
        >>> p3 = Parcel(3, 2, 'New York', 'Windsor')
        >>> t2.pack(p3)
        True
        >>> t2.fullness()
        10.0
        >>> t3 = Truck(1111, 50, 'Toronto')
        >>> f.add_truck(t3)
        >>> f.num_nonempty_trucks()
        2
        """
        count = 0
        for t in self.trucks:
            if t.fullness() > 0:
                count += 1
        return count

    def parcel_allocations(self) -> Dict[int, List[int]]:
        """Return a dictionary in which each key is the ID of a truck in this
        fleet and its value is a list of the IDs of the parcels packed onto it,
        in the order in which they were packed.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
        >>> p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.pack(p2)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.parcel_allocations() == {1423: [27, 12], 1333: [28]}
        True
        """
        d = {}
        for t in self.trucks:
            lst = []
            for p in t.parcels:
                lst.append(p.id)
            d[t.id] = lst
        return d

    def total_unused_space(self) -> int:
        """Return the total unused space, summed over all non-empty trucks in
        the fleet.
        If there are no non-empty trucks in the fleet, return 0.

        >>> f = Fleet()
        >>> f.total_unused_space()
        0
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.total_unused_space()
        995
        """
        s = 0
        for t in self.trucks:
            if t.fullness() > 0:
                s += t.get_available_capacity()
        return s

    def _total_fullness(self) -> float:
        """Return the sum of truck.fullness() for each non-empty truck in the
        fleet. If there are no non-empty trucks, return 0.

        >>> f = Fleet()
        >>> f._total_fullness() == 0.0
        True
        >>> t = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t)
        >>> f._total_fullness() == 0.0
        True
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f._total_fullness()
        50.0
        """
        count = 0
        for t in self.trucks:
            if t.fullness() > 0:
                count += t.fullness()
        return count

    def average_fullness(self) -> float:
        """Return the average percent fullness of all non-empty trucks in the
        fleet.

        Precondition: At least one truck is non-empty.

        >>> f = Fleet()
        >>> t = Truck(1423, 10, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.average_fullness()
        50.0
        """
        return self._total_fullness() / self.num_nonempty_trucks()

    def total_distance_travelled(self, dmap: DistanceMap) -> int:
        """Return the total distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Precondition: <dmap> contains all distances required to compute the
                      average distance travelled.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.total_distance_travelled(m)
        36
        """
        count = 0
        for t in self.trucks:
            current = t.depot
            for city in t.route:
                distance = dmap.distance(current, city)
                if distance >= 0:
                    count += distance
                current = city
            if len(t.route) > 0:
                count += dmap.distance(current, t.depot)
        return count

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the average distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Include in the average only trucks that have actually travelled some
        non-zero distance.

        Preconditions:
        - <dmap> contains all distances required to compute the average
          distance travelled.
        - At least one truck has travelled a non-zero distance.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.average_distance_travelled(m)
        18.0
        """
        count = 0
        for t in self.trucks:
            if t.fullness() > 0:
                count += 1
        return self.total_distance_travelled(dmap) / count


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
