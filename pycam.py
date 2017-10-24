import threading
import sys
from custom_transport import *
from rx import Observable, Observer

sys.path.insert(0, '/home/lz/Coding/python-onvif-zeep/onvif')
sys.path.insert(0, '/home/lz/Coding/python-rtsp-client')

from client import *

def log(a):
    print(a)

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

def load_camera_information(camera):
    id = 'Camera ' + str(camera['id'])
    log(id + ': ' + 'loading information...')
    mycam = ONVIFCamera(camera['ip'], 
                        camera['onvif_port'],
                        camera['username'], 
                        camera['password'],
                        camera['wsdl'], 
                        transport=SocksTransport)
    log(id + ': ' + 'getting capabilities...')
    resp = mycam.devicemgmt.GetCapabilities()
    if resp["Imaging"]:
        log(id + ': ' + 'supports imaging services')
        imaging_url = resp["Imaging"]["XAddr"]
    if resp["Media"]:
        log(id + ': ' + 'supports media services')
        log(id + ': ' + 'querying media services...')
        media_service = mycam.create_media_service()
        log(id + ': ' + 'querying profiles...')
        profiles = media_service.GetProfiles()
        # Use the first profile and Profiles have at least one
        token = profiles[0].token
        log(id + ': ' + 'getting system uri...')
        params = mycam.devicemgmt.create_type('GetSystemUris')
        resp = mycam.media.GetStreamUri({'StreamSetup':{'Stream':'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}, 'ProfileToken':token})
        camera['camera_information'] = {}
        camera['camera_information']['rtsp'] = resp["XAddr"]
    return camera

def negotiate_stream_parameters(camera):
    print(camera['camera_information'])
    return camera

def begin_stream(camera):
    return camera

#take_until(cancel_launch).\
#delay_with_selector(lambda s: Observable.timer(2**s*500))

launch_camera = Observable.\
        just(load_cameras()[0]).\
		do_action(load_camera_information).\
		do_action(negotiate_stream_parameters).\
		do_action(begin_stream)
		
launch_camera.subscribe(
            on_next=lambda s: print(s),
			on_completed=lambda: print('done'),
			on_error=lambda e: print(e)
			)