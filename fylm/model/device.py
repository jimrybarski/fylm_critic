from enum import Enum, unique


@unique
class Device(Enum):
    original = 1
    hexaplex = 2
    plinko = 3
    cerevisiae = 4

