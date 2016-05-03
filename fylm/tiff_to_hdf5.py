import tifffile
import h5py
import os
import warnings
warnings.filterwarnings("ignore")
from datetime import datetime
import numpy as np
from fylm.image import ImageStack

# This is a proof of concept.
# All we're going to do is take a directory (with tiffs in it) and make an h5 file.
# Nothing else.

# with ImageStack("/var/fylm3/FYLM-160329.h5") as stack:
#     print(stack.get())

with h5py.File("/var/fylm3/FYLM-160329.h5", "a") as h5:
    image = h5['/%d/%s/%d' % (2, "BF", 0)]['0'].attrs.keys()

    print(" ".join(image))

    # directory = "/var/fylm3/ome files/FYLM-160329_1"
    # for filename in sorted(os.listdir(directory)):
    #     tiff = tifffile.TiffFile(os.path.join(directory, filename))
    #     pixel_size_um = tiff.micromanager_metadata['summary']['PixelSize_um']
    #     for image in tiff:
    #         data = image.tags['micromanager_metadata'].value
    #         field_of_view = data['PositionIndex']
    #         channel = data['Channel']
    #         z_offset = data['SlicePosition']
    #         width = data['Width']
    #         height = data['Height']
    #         frame = data['FrameIndex']
    #         uuid = data['UUID']
    #         timestamp = int(datetime.strptime(data['Time'], "%Y-%m-%d %H:%M:%S %z").timestamp())
    #         exposure_ms = data['Exposure-ms']
    #         group = h5.require_group('/%d/%s/%d' % (field_of_view, channel, z_offset))
    #         dataset = group.create_dataset(str(frame), (height, width), dtype=np.uint16)
    #         dataset[...] = image.asarray()