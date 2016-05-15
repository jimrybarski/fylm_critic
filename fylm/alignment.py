import numpy as np


class RotationCorrector(object):
    def __init__(self):
        self._sampled_images = []

    def add_image(self, image: np.ndarray):
        self._sampled_images.append(image)


class FYLMRotationCorrector(RotationCorrector):
    pass