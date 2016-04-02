from model.coordinates import BoundingBox


class Movie(object):
    def __init__(self, bounding_box: BoundingBox):
        self._bounding_box = bounding_box
        self._channels = {'BF': 1.0}
        self._fill_missing_fluorescent_frames = False
        self._start = 0.0
        self._stop = float('inf')

    def channel(self, name: str, alpha: float=1.0):
        assert 0 <= alpha <= 1.0
        self._channels[name] = alpha
        return self

    def start(self, timestamp: float):
        assert timestamp < self._stop
        self._start = timestamp
        return self

    def stop(self, timestamp: float):
        assert timestamp > self._start
        self._stop = timestamp
        return self

    def fill_missing_fluorescent_frames(self):
        self._fill_missing_fluorescent_frames = True
        return self
