import sys
from custom_transport import *

sys.path.insert(0, '/home/lz/Coding/python-onvif-zeep/onvif')

from client import *

def load_cameras():
    import json
    with open('cameras.json') as data_file:    
        data = json.load(data_file)
    return data

wsdl = '/home/lz/Coding/python-onvif-zeep/wsdl'
user = ''
password = ''
host = 'localhost'
port = 1080

proxies = {
    'http': 'socks5://' + user + ':' + password + '@' + host + ':' + str(port),
    'https': 'socks5://' + user + ':' + password + '@' + host + ':' + str(port)
}

SocksTransport = CustomTransport(proxies)
cameras = load_cameras()
for camera in cameras:
    print('Connecting to ' + camera['name'] + '...')
    imaging_url = ''
    mycam = ONVIFCamera(camera['ip'], camera['onvif'], camera['username'], camera['password'], wsdl, transport=SocksTransport)
    resp = mycam.devicemgmt.GetCapabilities()
    if resp["Imaging"]:
        imaging_url = resp["Imaging"]["XAddr"]
    resp = mycam.devicemgmt.GetServiceCapabilities()
    print(resp)

