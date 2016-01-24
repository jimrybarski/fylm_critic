import logging
from nd2reader import Nd2
from model.stack import ImageStack
from service.registration import V1RegistrationAnalyzer
from service.rotation import V1RotationAnalyzer
from service.database import Database
from service.experiment import load_experiment
import matplotlib.pyplot as plt
plt.style.use('ggplot')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
log = logging.getLogger()
log.addHandler(stream_handler)
log.setLevel(logging.DEBUG)

log.debug("started ftest")
experiment = load_experiment("/var/experiment/")
database = Database(experiment.database_file)
registrations = database.registration.df

plt.figure()
plt.scatter(registrations['x'], registrations['y'])
plt.show()


# log.debug("making image stack")
# stack = ImageStack()
# for image in experiment.image_filenames:
#     stack.add(Nd2(image))
#
# log.debug("calculating offsets")
# reg = V1RegistrationAnalyzer()
# rot = V1RotationAnalyzer()
# rot_offsets = rot.determine_offsets(stack, '')
# reg_offsets = reg.determine_translation(stack, '')
#
# log.debug("done...saving now")
# database.save(rot_offsets)
# database.save(reg_offsets)
