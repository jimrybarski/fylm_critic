from fylm.model.coordinates import Point
from enum import Enum, unique


@unique
class FeatureType(Enum):
    """ The different types of features we will train the ML classifier on. """
    partial_septum = 1
    septum = 2
    old_pole = 3
    new_pole = 4
    pombe_tube = 5
    cerevisiae_tube = 6
    pombe_nucleus = 7
    fluorescent_blob = 8


class Feature(object):
    """ A putative feature at a single place in a single point in time. """
    def __init__(self,
                 kind: FeatureType,
                 field_of_view: int,
                 location: Point,
                 time_index: int,
                 timestamp: float):
        self._kind = kind
        self._field_of_view = field_of_view
        self._location = location
        self._time_index = time_index
        self._timestamp = timestamp
