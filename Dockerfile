FROM ubuntu:latest
MAINTAINER Lucas Zanella (me@lucaszanella.com)

ARG SIP_LINK=https://sourceforge.net/projects/pyqt/files/sip/sip-4.19.7/sip-4.19.7.tar.gz

ARG PYQT5_LINK=https://sourceforge.net/projects/pyqt/files/PyQt5/PyQt-5.10/PyQt5_gpl-5.10.tar.gz

RUN apt-get update \
    && apt-get install -y build-essential make wget \
    && python3 python3-dev python3-pip \
    && qt5-default \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

#SIP INSTALLAITON
RUN wget --progress=bar:force -O sip.tar.gz $SIP_LINK \
    && mkdir sip \
    && tar -xzvf sip.tar.gz -C sip --strip-components=1 \
    && rm sip.tar.gz \
    && cd sip \
    && python3 configure.py && make && make install \
    && cd .. \
    && rm -rf sip

#PYQT5 INSTALLAITON
RUN wget --progress=bar:force -O pyqt5.tar.gz $PYQT5_LINK \
    && mkdir pyqt5 \
    && tar -xzvf pyqt5.tar.gz -C pyqt5 --strip-components=1 \
    && rm pyqt5.tar.gz \
    && cd pyqt5 \
    && python3 configure.py && make && make install \
    && cd .. \
    && rm -rf pyqt5

WORKDIR /home/pycam

ENTRYPOINT "/bin/bash"
