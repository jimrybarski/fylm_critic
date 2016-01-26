import logging
from model.experiment import ExperimentFiles
from service.database import Database
from service import tools

log = logging.getLogger(__name__)


def run(experiment: ExperimentFiles):
    stack = tools.load_stack(experiment)
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
