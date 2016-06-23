from fylm.controller import preprocess
from fylm.model.device import Device

# the following will normally come from command line
tif_directory = '/home/jim/fylm3/1'
hdf5_filename = '/home/jim/fylm3/test.h5'
device = Device.original

# create an aligned image stack
preprocess.main(tif_directory, hdf5_filename, device)
