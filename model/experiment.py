from model import version
import re
import logging

log = logging.getLogger(__name__)


class ExperimentFiles(object):
    """ Models all the files related to a particular experiment. """
    def __init__(self, path: str):
        self._path = path.rstrip('/')
        self._date = None
        self._images = set()
        self._version = None

    @property
    def date(self) -> str:
        """ A six-digit string in the form YYMMDD representing a date. """
        if self._date is None:
            raise ValueError("You need to add some images to the experiment first.")
        return self._date

    @property
    def version(self):
        if self._version is None:
            return version
        return self._version

    @property
    def database_file(self) -> str:
        return self._make_filename('sqlite')

    @property
    def binary_data_file(self) -> str:
        return self._make_filename('h5')

    @property
    def metadata_file(self) -> str:
        return self._make_filename('json')

    def _make_filename(self, extension: str) -> str:
        return "{path}/{date}.{extension}".format(path=self._path,
                                                  date=self.date,
                                                  extension=extension)

    @property
    def image_files(self):
        yield from sorted(self._images)

    def add_image_file(self, filename: str):
        date = self._extract_date(filename)
        if self._date is None:
            self._date = date
        if date is not None and date == self._date:
            self._images.add("{path}/{filename}".format(path=self._path, filename=filename))
        else:
            log.warn("Found an invalid or improperly named ND2: {filename}".format(filename=filename))
            log.warn("Not adding {filename} to the experiment.".format(filename=filename))

    def set_metadata(self, metadata: dict):
        self._version = metadata.get('version', version)

    def _extract_date(self, filename: str) -> str:
        match = re.match(r'''^FYLM-(\d{6})-\d{3}.nd2$''', filename)
        return match.group(1) if match else None
