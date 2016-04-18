from fylm.model.roi import RegionOfInterest
from fylm.image import ImageStack
from typing import Union, List


class MovieCreator(object):
    """
    Combines data sources to produce frames of a movie.

    """
    def __init__(self, movie: Movie, rois: List[RegionOfInterest]):
        self._movie = movie
        self._rois = rois

    def __iter__(self):
        pass

    def __getitem__(self, item):
        pass


class FigureCreator(object):
    """
    Combines data sources to produce frames of a movie.

    """
    def __init__(self, figure: Figure, roi: RegionOfInterest):
        self._figure = figure


class Movie(object):
    """
    A description of a movie that you want to be created. Can be inserted into a larger movie.

    """
    def __init__(self):
        self._channels = set()

    def add_channel(self, channel: str):
        self._channels.add(channel)


class Figure(object):
    """
    A description of an image you want to be created.

    """
    def __init__(self):
        pass


class FeatureIndicator(object):
    """

    """
    pass


def save(image_stack: ImageStack, visualizations: List[Union[Movie, Figure]]):
    """
    Writes movies and figures to disk.

    Parameters
    ----------
    visualizations: a list of Movies and/or Figures

    """
    pass
