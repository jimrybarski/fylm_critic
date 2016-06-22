import numpy as np


def cw_rotate(image: np.ndarray) -> np.ndarray:
    assert image.shape[0] > 0 and image.shape[1] > 0
    return np.flipud(image).T


def ccw_rotate(image: np.ndarray) -> np.ndarray:
    assert image.shape[0] > 0 and image.shape[1] > 0
    return np.flipud(image.T)


def crop(image: np.ndarray, margin_percent: float) -> np.ndarray:
    assert image.shape[0] > 0 and image.shape[1] > 0
    height, width = image.shape
    margin = int(width * margin_percent)
    return image[:, margin: width - margin]
