from model.coordinates import BoundingBox
from model.image import Image


class Movie(object):
    def __init__(self, bounding_box: BoundingBox):
        self._bounding_box = bounding_box
        self._alphas = {}
        self._images = {}
        self._fill_missing_fluorescent_frames = False
        self._start = 0.0
        self._stop = float('inf')

    def channel(self, name: str, alpha: float=1.0):
        assert 0 <= alpha <= 1.0
        self._alphas[name] = alpha
        self._images[name] = None
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

    def offer_image(self, image: Image):
        if image.channel not in self._images:
            # We don't want this image
            return
        if self._images[image.channel] is not None:
            msg = 'A movie had not yet used an image from channel "%s" and was offered another image of that channel'
            raise RuntimeError(msg % image.channel)
        self._images[image.channel] = self._bounding_box.extract(image)

    def emit_frame(self):
        if not all(self._images.values()):
            return None
        # combine the images
