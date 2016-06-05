import numpy as np
import logging

log = logging.getLogger(__name__)


def normalize_image(image: np.ndarray) -> np.ndarray:
    return crop(cw_rotate(image))


def cw_rotate(image: np.ndarray) -> np.ndarray:
    return np.flipud(image).T


def ccw_rotate(image: np.ndarray) -> np.ndarray:
    return np.flipud(image.T)


def crop(image: np.ndarray) -> np.ndarray:
    # sometimes we snag corners, by cropping the left and right 10% of the image we focus only on the
    # vertical bars formed by the structure
    height, width = image.shape
    margin = int(width * 0.1)
    return image[:, margin: width - margin]
