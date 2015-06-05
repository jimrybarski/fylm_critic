from model.experiment import Experiment
from model.plan import Plan


experiment = Experiment("/home/jim/Desktop/fylm3/", "141111")
data_units_from_cli = ["first_frame", "rotation", "registration", "timestamp",
                       "location", "kymograph", "annotation", "movie",
                       "fluorescence", "puncta"]

plan = Plan(data_units_from_cli)
