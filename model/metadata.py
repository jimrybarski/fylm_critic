import json


class Metadata(object):
    """
    Stores mandatory user-supplied data about each experiment. Minimum loading time is when the user wants to consider
    the experiment to have begun (typically, this is less than an hour). The bright field name is the white light
    channel which is used in alignment and also for making figures. We also keep track of which versions we used for
    required analyses (registration, rotation, location of the catch channels, and annotation).

    """
    def __init__(self):
        self._data = {}

    def __repr__(self):
        return json.dumps(self._data)

    def load(self, raw_text: str):
        try:
            self._data = json.loads(raw_text)
        except ValueError:
            raise ValueError("Invalid or corrupt metadata file. ")

    @property
    def minimum_loading_time(self) -> float:
        return self._data.get('minimum_loading_time', 0.0)

    @minimum_loading_time.setter
    def minimum_loading_time(self, seconds: float):
        seconds = float(seconds)
        assert seconds >= 0.0
        self._data['minimum_loading_time'] = seconds

    @property
    def brightfield_name(self) -> str:
        try:
            return self._data['brightfield_name']
        except KeyError:
            raise KeyError("The name of the brightfield channel was not defined in the metadata.")

    @brightfield_name.setter
    def brightfield_name(self, name: str):
        self._data['brightfield_name'] = name

    def set_version(self, action_name: str, version: str):
        """ Stores the version used to run one of the basic analyses. """
        assert action_name in ('alignment', 'location', 'annotation'), "Invalid action. Must be one of: 'alignment', 'location', 'annotation'"
        assert version.count('.') == 2, "Invalid version number: {version} -- Should be formatted like 1.2.3".format(version=version)
        if 'versions' not in self._data.keys():
            self._data['versions'] = {}
        self._data['versions'][action_name] = version

    def get_version(self, action_name: str):
        # guaranteed to return the version number if it exists or None
        return self._data.get('versions', {}).get(action_name)
