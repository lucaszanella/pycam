xhost local:root && docker run --rm -it -v /tmp/.X11-unix:/tmp/.X11-unix -v /home/lz/pycam:/home/project -e DISPLAY=unix$DISPLAY pycam && xhost -
