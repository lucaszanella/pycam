#!/usr/bin/env python3
#Lucas Zanella - 2017
import sys
#sys.path.insert(0, '/home/lz/Coding/python-onvif-zeep/onvif')
sys.path.insert(0, '/home/deps/python-rtsp-client')
sys.path.insert(0, '/home/deps/python-native-nmap')
sys.path.insert(0, '/home/deps/PySocks')

import threading
import socks
import time
import re
import signal
#----------QT---------------
from PyQt5.QtWidgets import *
from PyQt5.QtQml import *
from PyQt5.QtCore import *
import sys
import resource_rc #resource needed for material theme
#---------------------------
from custom_transport import *
from camera import Camera
from pynmap import *
from time import sleep
from threading import Thread
from client import *
from rtsp import RTSPClient

signal.signal(signal.SIGINT, signal.SIG_DFL) #Control C closes window

#Socks configuration---------
#wsdl = '/home/deps/python-onvif-zeep/wsdl'

cam = Camera(id = '',
             ip = '192.168.1.173',
             onvif = '8080',
             rtsp = '554',
             username = 'admin',
             password = 'admin',
             socks = True
             )

app = QApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.load(QUrl('pycam.qml'))
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