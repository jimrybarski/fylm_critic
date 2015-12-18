from model.image.stack import ImageStack
from service.image.rotation import V1RotationAnalyzer
from service.image.registration import V1RegistrationAnalyzer
from model.image.offset import RegistrationOffsets
from nd2reader import Nd2
from skimage import io, transform
import logging
import time


log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


stack = ImageStack()
stack.add(Nd2("/var/nd2s/FYLM-141111-001.nd2"))


def show(image):
    io.imshow(image)
    io.show()
    time.sleep(0.2)

rot = V1RotationAnalyzer()
reg = V1RegistrationAnalyzer()
offsets = RegistrationOffsets()
reg.determine_translation(stack, offsets, 'BF')
for image in stack.select(z_levels=1, fields_of_view=3, channels='BF'):
    translation = offsets.get(image.field_of_view, image.frame_number)
    warp = transform.AffineTransform(translation=(-translation.x, -translation.y))
    timage = transform.warp(image, warp)
    tfname = "/var/nd2s/images/%s_%s.png" % (image.field_of_view, image.frame_number)
    log.debug(tfname)
    if image.frame_number == 1:
        break
    io.imsave(tfname, timage)
