import logging

from model.artist import XCrossArtist
from model.canvas import Canvas
from model.color import Color
from model.coordinates import Point
from nd2reader import Nd2
import numpy as np
from skimage import io
from model.stack import ImageStack
from service.registration import V1RegistrationAnalyzer
from service.rotation import V1RotationAnalyzer

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
log = logging.getLogger()
log.addHandler(stream_handler)
log.setLevel(logging.DEBUG)

log.debug("started ftest")
nd2 = Nd2("/var/nd2s/FYLM-141111-001.nd2")
reg = V1RegistrationAnalyzer()
rot = V1RotationAnalyzer()

stack = ImageStack()
stack.add(nd2)
log.debug("loaded images")

rot_offsets = rot.determine_offsets(stack, '')
log.debug("Finish rotation!!!!")
reg_offsets = reg.determine_translation(stack, '')
