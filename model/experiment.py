class Experiment(object):
    def __init__(self, base_path, date):
        assert len(date) == 6
        self._base_path = base_path
        self._date = date

    @property
    def data_file(self):
        tail = "/" if not self._base_path.endswith("/") else ""
        return self._base_path + tail + "%s.h5" % self._date