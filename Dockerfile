FROM ubuntu:bionic
MAINTAINER Lucas Zanella (me@lucaszanella.com)

RUN apt-get update \
    && apt-get install -y build-essential make wget ca-certificates \
    python3 python3-dev libgl1-mesa-dev python3-pyqt5 python3-pyqt5.qtquick \
    qt5-default qml-module-qtquick-controls2 libqt5qml5 qml-module-qtquick2 qml-module-qtquick-window2 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

#RUN apt-get install -y dbus-x11 && dbus-uuidgen > /var/lib/dbus/machine-id

#RUN git clone https://github.com/qt/qtquickcontrols2 \
#    && cd qtquickcontrols2 \
#    && qmake \
#    && make \
#    && make install


WORKDIR /home/project

ENTRYPOINT "/bin/bash"
