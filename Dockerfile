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
    pkg-config

RUN pip3 install --upgrade Cython \
    && pip3 install --upgrade scikit-image \
    && pip3 install git://github.com/jimrybarski/nd2reader@7f359bacc1aaac0900a51bd14d4b1fef777fe4db \
    && apt-get remove -y \
       build-essential \
       git \
       pkg-config \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

ONBUILD COPY . /opt/
