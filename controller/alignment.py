import logging
from model.experiment import ExperimentFiles
from model.stack import ImageStack
from nd2reader import Nd2
from service.database import Database

log = logging.getLogger(__name__)


def run(experiment: ExperimentFiles):
    stack = ImageStack()
    for image in experiment.image_filenames:
        stack.add(Nd2(image))

    log.info("Starting rotation correction.")
    rotation_offsets = experiment.rotation_analyzer.determine_offsets(stack, '')
    log.info("Rotation analysis complete.")

    log.info("Starting registration correction.")
    registration_offsets = experiment.registration_analyzer.determine_translation(stack, '')
    log.info("Registration analysis complete.")

    database = Database(experiment.database_file)
    log.info("Saving rotation offsets to the database.")
    database.save(rotation_offsets)
    log.info("Saving registration offsets to the database.")
    database.save(registration_offsets)
