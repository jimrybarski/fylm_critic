from nd2reader import Nd2
from model.experiment import ExperimentFiles
from model.stack import ImageStack
from service.database import Database
from service.registration import RegistrationCorrector
from service.rotation import RotationCorrector


def load_stack(experiment: ExperimentFiles):
    """ Populates an image stack with all images for an experiment and adds the alignment correctors, if available. """
    stack = ImageStack()
    for image in experiment.image_filenames:
        stack.add(Nd2(image))
    database = Database(experiment.database_file)
    registration_offsets = database.load_registration_offsets()
    rotation_offsets = database.load_rotation_offsets()
    registration_corrector = RegistrationCorrector(registration_offsets) if registration_offsets else None
    rotation_corrector = RotationCorrector(rotation_offsets) if rotation_offsets else None
    stack.set_correctors(registration_corrector=registration_corrector,
                         rotation_corrector=rotation_corrector)
    return stack
