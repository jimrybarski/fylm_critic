from model.tube import CatchTube
from model.image import Image
from typing import Union


class Movie(object):
    def __init__(self, region_of_interest: Union[CatchTube]):
        self._roi = region_of_interest
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
        """
        We need to see if this image belongs in the movie (e.g., it's a channel we're interested in, it's the right
        field of view, etc).

        """
        if image.channel not in self._images or image.field_of_view != self._roi.field_of_view:
            # We don't want this image
            return
        # We never evict fluorescent images if we're filling in missing frames, so we can only throw an error for
        # unexpected fluorescent images under very strict conditions. Still, it's unlikely that a bug will sneak through
        # here without affecting the bright field images, and also and go unnoticed when we actually view the movies
        invalid_fluorescent = image.channel != 'BF' and not self._fill_missing_fluorescent_frames and self._images[image.channel] is not None
        invalid_bf = image.channel == 'BF' and self._images[image.channel] is not None
        if invalid_fluorescent or invalid_bf:
            msg = 'A movie had not yet used an image from channel "%s" and was offered another image of that channel'
            raise RuntimeError(msg % image.channel)
        self._images[image.channel] = self._roi.extract(image)

    def emit_frame(self):
        if not all([i is not None for i in self._images.values()]):
            return None
        # combine the images
        combined_image = "woo"
        # delete images we no longer need
        for key in self._images:
            if key == 'BF' or not self._fill_missing_fluorescent_frames:
                self._images[key] = None
        return combined_image
