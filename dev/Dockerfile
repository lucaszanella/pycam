FROM ubuntu:bionic
MAINTAINER Lucas Zanella (me@lucaszanella.com)

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3 python3-pyqt5 python3-pyqt5.qtquick python3-pip git python3-setuptools \
    qt5-default qml-module-qtquick-controls2 libqt5qml5 qml-module-qtquick2 qml-module-qtquick-window2

RUN mkdir -p /home/deps && cd /home/deps  \
    && git clone https://github.com/lucaszanella/PySocks \
    && git clone https://github.com/lucaszanella/python-rtsp-client \
    && git clone https://github.com/lucaszanella/python-native-nmap && cd python-native-nmap && git checkout 45c73976f50134a89009d38c5763501bcaea0199 && cd .. \
    && git clone https://github.com/killian441/python-rtsp-client python-rtsp-client-orig \
    && git clone https://github.com/mvantellingen/python-zeep \
    && cd python-zeep && git checkout 2421b3419514ce1e0e2ff8d7c7a3a434f13aaf8 && python3 setup.py install && cd .. && rm -rf python-zeep \
    && git clone https://github.com/lucaszanella/python-onvif-zeep 
    
    #&& cd python-onvif-zeep && python3 setup.py install && cd .. && rm -rf python-onvif-zeep

WORKDIR /home/project/src

ENTRYPOINT "/bin/bash"
