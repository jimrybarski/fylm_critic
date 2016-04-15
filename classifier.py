from abc import abstractmethod


class ImageFeatureDetector(object):
    """
    Interface for all detectors that find features in single images.

    """
    pass


class SVM(ImageFeatureDetector):
    """
    Finds features in an image by convoluting a support vector machine kernel.

    """
    pass
