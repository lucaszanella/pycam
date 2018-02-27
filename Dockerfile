FROM ubuntu:bionic
MAINTAINER Lucas Zanella (me@lucaszanella.com)

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3 python3-pyqt5 python3-pyqt5.qtquick python3-pip git python3-setuptools \
    qt5-default qml-module-qtquick-controls2 libqt5qml5 qml-module-qtquick2 qml-module-qtquick-window2

RUN mkdir -p /home/deps && cd /home/deps \
    && git clone https://github.com/lucaszanella/PySocks \
    && git clone https://github.com/lucaszanella/python-rtsp-client \
    && git clone https://github.com/lucaszanella/python-native-nmap \
    && git clone https://github.com/lucaszanella/python-onvif-zeep \
    && cd python-onvif-zeep && python3 setup.py install && cd .. && rm -rf python-onvif-zeep

WORKDIR /home/project

ENTRYPOINT "/bin/bash"
