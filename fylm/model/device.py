from enum import Enum, unique


@unique
class Device(Enum):
    original = 1
    plinko = 2
    cerevisiae = 3
