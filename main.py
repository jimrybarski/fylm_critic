from fylm.controller import preprocess
from fylm.model.device import Device

tif_directory = '/var/fylm3/ome files/FYLM-160329_1/'
hdf5_filename = '/var/fylm3/test.h5'
device = Device.original
preprocess.main(tif_directory, hdf5_filename, device)
