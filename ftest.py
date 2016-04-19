from fylm.model.roi import RegionOfInterest
from fylm.model.coordinates import Point
from fylm.visualization import Movie, Figure, MovieCreator
from fylm.image import ImageStack

image_stack = ImageStack("/var/experiment/161010.h5")


# typical! but we can also stream a single movie if we want
tube1 = RegionOfInterest(1, 3, Point(3, 4), Point(1, 2))
tube2 = RegionOfInterest(1, 3, Point(12, 7), Point(5, 8))
movie = Movie()
mc = MovieCreator(movie, [tube1, tube2])
