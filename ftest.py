from model.image.stack import ImageStack
from service.image.registration import V1RegistrationAnalyzer
from service.image.rotation import V1RotationAnalyzer
from model.image.offset import RotationOffsets
from nd2reader import Nd2
from skimage import io, transform
import logging

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


stack = ImageStack()
stack.add(Nd2("/var/nd2s/FYLM-141111-001.nd2"))
log.debug("Added nd2")

reg = V1RotationAnalyzer()
offsets = RotationOffsets()
reg.determine_offsets(stack, offsets, 'BF')
for image in stack.filter(z_level=1, channel="BF"):
    skew = offsets.get(image.field_of_view)
    timage = transform.rotate(image, skew)
    fname = "/var/nd2s/images/%s_%s_original.png" % (image.field_of_view, image.frame_number)
    tfname = "/var/nd2s/images/%s_%s_rotated.png" % (image.field_of_view, image.frame_number)
    log.debug(tfname)
    io.imsave(tfname, timage)
    io.imsave(fname, image)
    if image.frame_number == 1:
        break