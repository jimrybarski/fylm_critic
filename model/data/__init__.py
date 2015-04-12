from service.io import DataIO
from tables import IsDescription


class DataFactory(object):
    def create(self, name):
        data_unit = {"first_frame": FirstFrameData,
                     "rotation": RotationData,
                     "registration": RegistrationData,
                     "timestamp": TimestampData,
                     "location": LocationData,
                     "kymograph": KymographData,
                     "annotation": AnnotationData,
                     "movie": MovieData,
                     "fluorescence": FluorescenceData,
                     "puncta": PunctaData
                     }

        return data_unit[name]()


class BaseData(object):
    def __init__(self):
        self._dependencies = None
        self._name = None
        self._source = None

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def name(self):
        return self._name

    @property
    def source(self):
        return self._source


class FirstFrameData(BaseData):
    def __init__(self):
        super(FirstFrameData, self).__init__()
        self._dependencies = None
        self._name = "first_frame"
        self._source = "first_nd2_frame"


class RotationData(BaseData):
    def __init__(self):
        super(RotationData, self).__init__()
        self._dependencies = None
        self._name = "rotation"
        self._source = "first_nd2_frame"


class RegistrationData(BaseData):
    def __init__(self):
        super(RegistrationData, self).__init__()
        self._dependencies = ["first_frame"]
        self._name = "registration"
        self._source = "nd2"


class TimestampData(BaseData):
    def __init__(self):
        super(TimestampData, self).__init__()
        self._dependencies = None
        self._name = "timestamp"
        self._source = "nd2"
        self._data = {}


class LocationData(BaseData):
    def __init__(self):
        super(LocationData, self).__init__()
        self._dependencies = ["first_frame", "rotation"]
        self._name = "location"
        self._source = "nd2"


class KymographData(BaseData):
    def __init__(self):
        super(KymographData, self).__init__()
        self._dependencies = ["location"]
        self._name = "kymograph"
        self._source = "image_reader"


class AnnotationData(BaseData):
    def __init__(self):
        super(AnnotationData, self).__init__()
        self._dependencies = ["kymograph"]
        self._name = "annotation"
        self._source = "image_reader"
    

class MovieData(BaseData):
    def __init__(self):
        super(MovieData, self).__init__()
        self._dependencies = None
        self._name = "movie"
        self._source = "image_reader"


class FluorescenceData(BaseData):
    def __init__(self):
        super(FluorescenceData, self).__init__()
        self._dependencies = ["annotation"]
        self._name = "fluorescence"
        self._source = "image_reader"


class PunctaData(BaseData):
    def __init__(self):
        super(PunctaData, self).__init__()
        self._dependencies = ["annotation"]
        self._name = "puncta"
        self._source = "image_reader"