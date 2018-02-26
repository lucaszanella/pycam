FROM ubuntu:bionic
MAINTAINER Lucas Zanella (me@lucaszanella.com)

RUN apt-get update \
    && apt-get install -y \
    python3 python3-pyqt5 python3-pyqt5.qtquick \
    qt5-default qml-module-qtquick-controls2 libqt5qml5 qml-module-qtquick2 qml-module-qtquick-window2 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/project

ENTRYPOINT "/bin/bash"
