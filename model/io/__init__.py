from abc import abstractmethod
import tables


class BaseDataIO(object):
    def __init__(self, file_handle):
        self._fh = file_handle

    @abstractmethod
    def create(self, *args):
        raise NotImplemented

    @abstractmethod
    def load(self, data_unit):
        raise NotImplemented

    @abstractmethod
    def save(self, data_unit):
        raise NotImplemented


class FirstFrameIO(BaseDataIO):
    def create(self, nd2):
        atom = tables.Atom.from_dtype(nd2.dtype)
        self._fh.createCArray(self._fh.root, 'first_frame', atom, nd2.shape)
        self._fh.flush()

    def load(self, data_unit):
        data_unit.data = self._fh.root.first_frame[:]

    def save(self, data_unit):
        self._fh.root.first_frame[:] = data_unit.data
        self._fh.flush()