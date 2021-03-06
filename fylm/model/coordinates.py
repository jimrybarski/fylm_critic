class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other: 'Point'):
        return self.x == other.x and self.y == other.y
