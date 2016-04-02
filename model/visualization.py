from model.tube import CatchTube
from model.image import Image
from model.color import Color, convert_to_rgb
from typing import Union


class BaseVisualization(object):
    def __init__(self, region_of_interest: Union[CatchTube]):
        self._roi = region_of_interest
        self._channels = {}

    def add_channel(self, name: str, color: Color=Color(255, 255, 255), alpha: float=1.0):
        assert 0 <= alpha <= 1.0
        self._channels[name] = (alpha, color)
        return self

    @property
    def channels(self):
        return self._channels

    @property
    def region_of_interest(self):
        return self._roi

    @property
    def field_of_view(self):
        return self._roi.field_of_view

    @property
    def should_fill_missing_fluorescent_frames(self):
        # we will only ever need this in Movies
        return False


class Figure(BaseVisualization):
    """
    Defines a single still image, usually for a paper figure.

    """
    def __init__(self, region_of_interest: Union[CatchTube]):
        super().__init__(region_of_interest)
        self._timestamp = None

    def set_timestamp(self, timestamp: float):
        assert 0.0 <= timestamp
        self._timestamp = timestamp


class Movie(BaseVisualization):
    """
    Defines a movie to be made, typically for a supplemental figure.

    """
    def __init__(self, region_of_interest: Union[CatchTube]):
        super().__init__(region_of_interest)
        self._missing_fl_fill = False
        self._start = 0.0
        self._stop = float('inf')
    
    def set_start(self, timestamp: float):
        assert timestamp < self._stop
        self._start = timestamp
        return self

    def set_stop(self, timestamp: float):
        assert timestamp > self._start
        self._stop = timestamp
        return self

    def fill_missing_fluorescent_frames(self):
        self._missing_fl_fill = True
        return self
    
    @property
    def start(self):
        return self._start
    
    @property
    def stop(self):
        return self._stop
    
    @property
    def should_fill_missing_fluorescent_frames(self):
        return self._missing_fl_fill


class FigureBuilder(object):
    """
    Combines image data with annotations and markup to produce frames for movies and images for figures.
    
    """
    def __init__(self, description: Union[Movie, Figure]):
        self._description = description
        self._images = {channel: None for channel in self._description.channels}
        
    def offer_image(self, image: Image):
        """
        We need to see if this image belongs (e.g., it's a channel we're interested in, it's the right
        field of view, etc).

        """
        if image.channel not in self._images or image.field_of_view != self._description.field_of_view:
            # We don't want this image
            return
        invalid_brightfield = image.channel == 'BF' and self._images[image.channel] is not None
        if invalid_brightfield:
            msg = 'A figure was offered a new image before the last one was used.'
            raise RuntimeError(msg % image.channel)
        self._images[image.channel] = self._description.region_of_interest.extract(image)

    def build(self):
        if not all((i is not None for i in self._images.values())):
            return None

        # combine the images
        combined_image = convert_to_rgb(self._images['BF'])
        for channel, image in self._images.items():
            color, alpha = self._description.channels[channel]
            combined_image += color.convert(image) * alpha

        # delete images we no longer need
        for key in self._images:
            if key == 'BF' or not self._description.should_fill_missing_fluorescent_frames:
                self._images[key] = None
        return combined_image
