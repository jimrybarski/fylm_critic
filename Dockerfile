FROM debian:jessie
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
    libjpeg-dev \
    pkg-config \
    && pip3 install --upgrade \
        nd2reader \
        scikit-image \
    && apt-get remove -y \
       build-essential \
       pkg-config \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

ONBUILD COPY . /opt/