from fylm.model.device import Device
import numpy as np
import logging

log = logging.getLogger(__name__)


def normalize_image(image: np.ndarray, device: Device) -> np.ndarray:
    if device == Device.original:
        return crop(cw_rotate(image), 0.1)
    else:
        raise ValueError("Normalizing image not implemented for your device")


def cw_rotate(image: np.ndarray) -> np.ndarray:
    return np.flipud(image).T


def ccw_rotate(image: np.ndarray) -> np.ndarray:
    return np.flipud(image.T)


def crop(image: np.ndarray, margin_percent: float) -> np.ndarray:
    # sometimes we snag corners, by cropping the left and right 10% of the image we focus only on the
    # vertical bars formed by the structure
    height, width = image.shape
    margin = int(width * margin_percent)
    return image[:, margin: width - margin]
