USER_=$USER
#Used to intercept a package so I can edit live while testing. 
#Then it's just a matter of sending to github and rebuilding the docker with no cache.
INSERT_LOCAL="-v /home/$USER_/python-rtsp-client:/home/deps/python-rtsp-client"
#INSERT_LOCAL=
xhost local:root && docker run --rm -it -v /tmp/.X11-unix:/tmp/.X11-unix -v /home/$USER_/pycam:/home/project $(echo $INSERT_LOCAL) -e DISPLAY=unix$DISPLAY pycam && xhost -
