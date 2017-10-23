import sys
from custom_transport import *

sys.path.insert(0, '/home/lz/Coding/python-onvif-zeep/onvif')

from client import *

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
mycam = ONVIFCamera('192.168.1.164', 1018, 'admin', '888888', wsdl, transport=SocksTransport)
resp = mycam.devicemgmt.GetHostname()
print(resp)