#!/usr/bin/env python3
#Lucas Zanella - 2017
import sys
sys.path.insert(0, '/home/deps/python-native-nmap')

import threading
import time
import re
import signal
#----------QT---------------
from PyQt5.QtWidgets import *
from PyQt5.QtQml import *
from PyQt5.QtCore import *
import resource_rc #resource needed for material theme
#---------------------------
from camera import Camera
from pynmap import *
from time import sleep
from threading import Thread

signal.signal(signal.SIGINT, signal.SIG_DFL) #Control C closes window

#Used for debug on MY specfic computer with my specific cameras
P=False
if len(sys.argv)>1 and sys.argv[1]=='lz':
    print("Lucas Zanella debug activated")
    from cameras import cams
    P=True

cam = Camera(id = '1',
             name = 'Teste',
             ip = '192.168.1.43',
             onvif = '1018',
             #rtsp = '10554',
             username = 'admin',
             password = '888888',
             socks = None
#             socks = {'user': '', 
#                      'password': '', 
#                      'host': '127.0.0.1', 
#                      'port': 1080}
             )

if P:
    cam = cams[0]
cam.probe_information()
for profile in cam.profiles:
    cam.rtsp_connect(profile.rtsp_uri)

app = QApplication(sys.argv)
engine = QQmlApplicationEngine()
#engine.load(QUrl('pycam.qml'))
#sys.exit(app.exec_())

"""
#proxy = {'socks_user': socks_user, 'socks_password': socks_password, 'socks_host': socks_host, 'socks_port': socks_port}
#nmap = Nmap(proxy=proxy)
#nmap = Nmap()

print("map scanning...")
ports=[80, 81, 8080]
cams = nmap.scan(addresses="192.168.1.0/24", ports=ports)
#ignore_these = [11, -2]
allow_these = [-1, 0]
cams = [x for x in cams.items() if x[1] in allow_these]
cams = [x[0] for x in cams]
cams_ips = [x.split(":")[0] for x in cams]
eliminate_these = ['192.168.1.0', '192.168.1.1', '192.168.1.255']
cams_ips = [x for x in cams_ips if x not in eliminate_these]
#https://repl.it/repls/SubmissiveColossalCaribou

#cams_ips = [{'id': '', 'ip': x, 'onvif': '', 'rtsp': '', 'username': '', 'password': ''} for x in cams_ips]
print(cams_ips)
"""
