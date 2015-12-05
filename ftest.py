from model.image.stack import ImageStack
from service.image.registration import V1RegistrationAnalyzer
from model.image.offset import Offsets
from nd2reader import Nd2
import logging

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


stack = ImageStack()
stack.add(Nd2("/var/nd2s/FYLM-141111-001.nd2"))
log.debug("Added nd2")

reg = V1RegistrationAnalyzer()
offsets = Offsets()
reg.determine_translation(stack, offsets, 'BF')
from pprint import pprint
pprint(offsets._offsets)
