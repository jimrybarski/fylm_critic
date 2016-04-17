from fylm.model.device import Device
import matplotlib.pyplot as plt
import logging

plt.style.use('ggplot')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
log = logging.getLogger()
log.addHandler(stream_handler)
log.setLevel(logging.DEBUG)
