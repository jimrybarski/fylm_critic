from model.data import DataFactory


class Plan(object):
    def __init__(self, data_unit_names):
        self._data_units = []
        factory = DataFactory()
        for name in data_unit_names:
            data_unit = factory.create(name)
            self._data_units.append(data_unit)