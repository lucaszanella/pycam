xhost local:root && sudo docker run --rm -it -v /tmp/.X11-unix:/tmp/.X11-unix -v /home/lz/pycam/lab4:/home/project -e DISPLAY=unix$DISPLAY lab5-pyqt-pycam && xhost -
