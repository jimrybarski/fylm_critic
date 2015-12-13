FROM debian:jessie
MAINTAINER Jim Rybarski <jim@rybarski.com>

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    python3-dev \
    python3-numpy \
    python3-pip \
    python3-h5py \
    python3-scipy \
    python3-skimage \
    libfreetype6-dev \
    python3-matplotlib \
    python3-pyqt5 \
    libpng-dev \
    libjpeg-dev \
    pkg-config \
    && pip3 install --upgrade Cython \
    && pip3 install --upgrade scikit-image \
    && pip3 install git+git://github.com/jimrybarski/nd2reader@ad9cdcd2ade44832ff09e1e0f43b673fde4ede17 \
    && apt-get remove -y \
       build-essential \
       git \
       pkg-config \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

ONBUILD COPY . /opt/
WORKDIR /opt