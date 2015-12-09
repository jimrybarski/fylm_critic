from model.image.stack import ImageStack
from service.image.registration import V1RegistrationAnalyzer
from model.image.offset import Offsets
from nd2reader import Nd2
from skimage import io, transform
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
for image in stack.filter(field_of_view=3, z_level=0, channel="BF"):
    dx, dy = offsets.get(image.field_of_view, image.frame_number)
    timage = transform.warp(image, transform.AffineTransform(translation=(-dx, -dy)))
    fname = "/var/nd2s/images/%s_%s.png" % (image.field_of_view, image.frame_number)
    log.debug(fname)
    io.imsave(fname, timage)
