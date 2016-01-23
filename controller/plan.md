# Controllers

These receive a database interface object, an image reader object, and optionally some arguments, with a few
exceptions.

  - init: looks for existing DB files and image files, figure out state of processing
  - preprocess: registration and rotation correction
  - analyze: define the locations of channels, and figure out if they have cells in them
             define the sizes and positions of cells
             extracts information from defined cells (fluorescence, puncta, etc.)
             make kymographs from old pole cells
  - train: select data for supervised learning processes
