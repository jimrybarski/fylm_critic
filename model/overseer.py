from abc import abstractmethod


class BaseOverseer(object):
    def __init__(self):
        self._source = None
        self._work_units = []

    def set_source(self, source):
        self._source = source

    @abstractmethod
    def run(self):
        raise NotImplemented