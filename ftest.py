from fylm.model.roi import RegionOfInterest
from fylm.model.coordinates import Point
from fylm.visualization import Movie, Figure, MovieCreator, save
from fylm.image import ImageStack, ROIStack

image_stack = ImageStack("/var/experiment/161010.h5")


figs = [Movie(),
        Movie(),
        Movie(),
        Movie(),
        Figure()]

save(image_stack, figs)


# typical! but we can also stream a single movie if we want
tube = RegionOfInterest(1, 3, Point(3, 4), Point(1, 2))
movie = Movie()
mc = MovieCreator(movie, tube)
