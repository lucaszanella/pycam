xhost local:root && docker run --rm -it --net=host -v /tmp/.X11-unix:/tmp/.X11-unix -v /home/$USER/pycam/src:/home/project -e DISPLAY=unix$DISPLAY pycam && xhost -
