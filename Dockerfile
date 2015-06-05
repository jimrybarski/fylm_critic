FROM ubuntu:15.04
MAINTAINER Jim Rybarski <jim@rybarski.com>

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  python3-dev \
  python3-numpy \
  python3-pip \
  python3-tables \
  python3-scipy \
  python3-skimage \
  libfreetype6-dev \
  python3-matplotlib \
  python3-pyqt5 \
  libfreetype6-dev \
  libpng-dev \
  libjpeg8-dev \ 
  pkg-config

RUN pip3 install \
  nd2reader

# Get cross-correlation registration method
RUN pip3 install --upgrade scikit-image
