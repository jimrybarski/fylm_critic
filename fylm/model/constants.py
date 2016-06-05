from enum import unique, IntEnum

FIFTEEN_DEGREES_IN_RADIANS = 0.262
ACCEPTABLE_SKEW_THRESHOLD = 5.0


@unique
class RotationDirection(IntEnum):
    no_rotation = 0
    clockwise = 1
    counterclockwise = 2
