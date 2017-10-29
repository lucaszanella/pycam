#!/usr/bin/env python3
import threading
import sys
import socks
import time
import re
from custom_transport import *
from rx import Observable, Observer

sys.path.insert(0, '/home/lz/Coding/python-onvif-zeep/onvif')
sys.path.insert(0, '/home/lz/Coding/python-rtsp-client')

from client import *
from rtsp import RTSPClient

def load_cameras():
    import json
    with open('cameras.json') as data_file:    
        data = json.load(data_file)
    return data

#Socks configuration---------
wsdl = '/home/lz/Coding/python-onvif-zeep/wsdl'
user = ''
password = ''
host = 'localhost'
port = 1080

proxies = {
    'http': 'socks5://' + user + ':' + password + '@' + host + ':' + str(port),
    'https': 'socks5://' + user + ':' + password + '@' + host + ':' + str(port)
}
#----------------------------
SocksTransport = CustomTransport(proxies)
thread_list = []

class Camera():
    def __init__(self, id=None, ip=None, onvif=None, rtsp=None, username=None, password=None):
        self.id = id
        self.ip = ip
        self.onvif = onvif
        self.rtsp = rtsp
        self.username = username
        self.password = password
        self.rtsp_uri = None
    def log(self, info):
        print('Camera ' + str(self.id) + ': ' + info)    


def load_camera_information(camera):
    camera.log('loading information...')
    camera.log('IP: ' + camera.ip + ', ONVIF: ' + str(camera.onvif))
    mycam = ONVIFCamera(camera.ip, 
                        camera.onvif,
                        camera.username, 
                        camera.password,
                        wsdl, 
                        transport=SocksTransport)
    camera.log('getting capabilities...')
    resp = mycam.devicemgmt.GetCapabilities()
    if resp["Imaging"]:
        camera.log('supports imaging services')
        imaging_url = resp["Imaging"]["XAddr"]
    if resp["Media"]:
        camera.log('supports media services')
        camera.log('querying media services...')
        media_service = mycam.create_media_service()
        camera.log('querying profiles...')
        profiles = media_service.GetProfiles()
        # Use the first profile and Profiles have at least one
        token = profiles[0].token
        camera.log('getting system uri...')
        params = mycam.devicemgmt.create_type('GetSystemUris')
        resp = mycam.media.GetStreamUri({'StreamSetup':{'Stream':'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}, 'ProfileToken':token})
        #print(resp)
        camera.rtsp_uri = resp["Uri"]
    return camera

def decide_streaming(rtsp_body):
    m = re.findall(r'm=.+', rtsp_body)
    a = re.findall(r'a=.+', rtsp_body)
    print(m)
    print(a)
    #print(re.findall(r'm=.+', rtsp_body))
    #print('decide between these: ' + rtsp_body())

def callback(s):
    #print(s)
    pass

def rtsp_connect(camera):
    url = camera.rtsp_uri#.replace('554\/11', '10554')
    camera.log('opening RTSP connection to url ' + url + ' ...')

    s = socks.socksocket() # Same API as socket.socket in the standard lib
    s.set_proxy(socks.SOCKS5, "localhost") # (socks.SOCKS5, "localhost", 1234)

    myrtsp = RTSPClient(url=url,callback=callback, socks=s, process_describe_response=decide_streaming)
    try:
        myrtsp.do_describe()
        while myrtsp.state != 'describe':
            time.sleep(0.1)
        myrtsp.do_setup('0')
        while myrtsp.state != 'setup':
            time.sleep(0.1)
        #Open socket to capture frames here
        myrtsp.do_play(myrtsp.cur_range, myrtsp.cur_scale)
    except Exception as e:
        print('EXCEPTION ------------------------------')
        print(e)
        myrtsp.do_teardown()
    return camera

def begin_stream(camera):
    return camera

#take_until(cancel_launch).\
#delay_with_selector(lambda s: Observable.timer(2**s*500))

example_of_camera = load_cameras()[0]
example_of_camera = Camera(
                            id = example_of_camera['id'],
                            ip = example_of_camera['ip'],
                            onvif = example_of_camera['onvif'],
                            rtsp = example_of_camera['rtsp'],
                            username = example_of_camera['username'],
                            password = example_of_camera['password']
                            )

launch_camera = Observable.\
        just(example_of_camera).\
		do_action(load_camera_information).\
		do_action(rtsp_connect).\
		do_action(begin_stream)
		
launch_camera.subscribe(
                        #on_next=lambda s: print(s),
                        on_completed=lambda: print('exit'),
                        on_error=lambda e: print(e)
                        )