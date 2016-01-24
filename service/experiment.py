from model.experiment import ExperimentFiles
import json
import os
import logging

log = logging.getLogger(__name__)


def load_experiment(device: int, path: str):
    # First look for any images in the directory
    experiment = ExperimentFiles(device, path)
    for file in os.listdir(path):
        if file.endswith('.nd2'):
            experiment.add_image_file(file)
    # Now try to read the metadata. Currently this only contains the version number used to process the data.
    try:
        with open(experiment.metadata_file) as f:
            metadata = json.loads(f.read())
    except FileNotFoundError:
        metadata = {}
    except ValueError:
        log.warn("Metadata file was corrupt. Acting as if there is no metadata.")
        metadata = {}
    experiment.set_metadata(metadata)
    return experiment
