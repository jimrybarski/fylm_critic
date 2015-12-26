FROM python:3.5-slim
MAINTAINER Jim Rybarski <jim@rybarski.com>

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gfortran \
        gcc \
        git \
        libgl1-mesa-dri \
        libgl1-mesa-swx11 \
        libosmesa6 \
        libfreetype6-dev \
        libpng12-dev \
        libjpeg-dev \
        pkg-config \
        libc6 \
        liblapack3 \
        liblapack-dev \
        libatlas3-base \
        libatlas-base-dev \
        libblas3 \
        libopenblas-base \
        libopenblas-dev \
        libhdf5-8 \
        libhdf5-mpich-8 \
        libhdf5-openmpi-8 \
        libhdf5-dev \
        libgcc1 \
        libgfortran3 \
        libstdc++6 \
        libumfpack5.6.2 \
        libfreeimage3 \
        libfreetype6 \
        libpng12-0 \
        libtcl8.6 \
        libtk8.6 \
        dvipng \
        ghostscript \
        texlive-extra-utils \
        texlive-latex-extra \
        ttf-staypuft \
        qt5-default \
        qtbase5-dev \
        qt5-qmake \
        libqt5core5a \
        libqt5dbus5 \
        libqt5designer5 \
        libqt5gui5 \
        libqt5help5 \
        libqt5network5 \
        libqt5printsupport5 \
        libqt5test5 \
        libqt5widgets5 \
        libqt5core5a \
        wget \
    && pip3 install \
        numpy \
        scipy \
        matplotlib \
        h5py \
    && wget http://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.5.1/PyQt-gpl-5.5.1.tar.gz \
    && wget http://sourceforge.net/projects/pyqt/files/sip/sip-4.17/sip-4.17.tar.gz \
    && tar -xf sip-4.17.tar.gz \
    && tar -xf PyQt-gpl-5.5.1.tar.gz \
    && cd sip-4.17 && python3.5 configure.py && make && make install && cd .. && rm -rf sip-4.17.tar.gz sip-4.17 \
    && cd PyQt-gpl-5.5.1 && yes yes | python3.5 configure.py && make && make install && cd .. && rm -rf PyQt-gpl-5.5.1.tar.gz PyQt-gpl-5.5.1 \
    && pip3 install --upgrade Cython \
    && pip3 install --upgrade scikit-image \
    && pip3 install "nd2reader==2.0.0" \
    && apt-get remove -y \
        wget \
        build-essential \
        gcc \
        gfortran \
        git \
        pkg-config \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*


RUN mkdir -p /root/.config/matplotlib/
COPY matplotlibrc /root/.config/matplotlib/matplotlibrc
ONBUILD COPY . /opt/
WORKDIR /opt