# Controllers

These receive a database interface object, an image reader object, and optionally some arguments, with a few
exceptions.

  - init: looks for existing DB files and image files, figure out state of processing
  - preprocess: registration and rotation correction
  - location: define the locations of channels, and figure out if they have cells in them
  - track: define the sizes and positions of cells
  - kymograph: make kymographs from old pole cells
  - movie: makes movies
  - analyze: extracts information from defined cells (fluorescence, puncta, etc.)