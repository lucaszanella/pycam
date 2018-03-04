import sys
sys.path.insert(0, '/home/deps/python-onvif-zeep/onvif')
sys.path.insert(0, '/home/deps/python-rtsp-client')
#sys.path.insert(0, '/home/deps/python-rtsp-client-orig')
sys.path.insert(0, '/home/deps/python-native-nmap')
sys.path.insert(0, '/home/deps/PySocks')
wsdl = '/home/deps/python-onvif-zeep/wsdl'

from custom_transport import *
from client import *
from rtsp import RTSPClient
import socks
import time
import re


class Profile(object):
    pass

class Camera():
    def __init__(self, id=None, name=None, ip=None, onvif=None, rtsp=None, username=None, password=None, socks=None):
        self.id = id
        self.name = name or ''
        self.ip = ip
        self.onvif = onvif
        self.rtsp = rtsp
        self.username = username
        self.password = password
        self.rtsp_uri = None
        self.profiles = []
        self.socks_transport = None
        self.socks = False
        if socks:
            self.socks = True
            self.socks_user = socks['user'] or ''
            self.socks_password = socks['password'] or ''
            self.socks_host = socks['host']
            self.socks_port = socks['port'] or 1080

            proxies = {
                'http': 'socks5://' + self.socks_user + ':' + self.socks_password + '@' + self.socks_host + ':' + str(self.socks_port),
                'https': 'socks5://' + self.socks_user + ':' + self.socks_password + '@' + self.socks_host + ':' + str(self.socks_port)
            }

            self.socks_transport = CustomTransport(timeout=10, proxies=proxies)
        
    def log(self, info):
        socks_info = ''
        if self.socks_transport: socks_info = ', socks://' + self.socks_host + ":" + str(self.socks_port)
        print('Camera ' + self.name + ', id: ' + str(self.id) + ', ' + self.ip + ':' + self.onvif + socks_info + ": " + str(info))

    def probe_information(self):
        self.log('loading information...')
        
        mycam = ONVIFCamera(self.ip, 
                            self.onvif,
                            self.username, 
                            self.password,
                            wsdl, 
                            transport=self.socks_transport
                            )
        self.log('getting capabilities...')
        resp = mycam.devicemgmt.GetCapabilities()

        if resp["Imaging"]:
            self.log('supports imaging services')
            self.imaging_url = resp["Imaging"]["XAddr"]
        if resp["Media"]:
            self.log('supports media services')
            self.log('querying media services...')
            media_service = mycam.create_media_service()
            self.log('querying profiles...')
            profiles = media_service.GetProfiles()
            for profile in profiles:
                p = Profile()
                p.name = profile.Name
                p.token = profile.token
                p.encoding = profile.VideoEncoderConfiguration.Encoding
                p.resolution_W = profile.VideoEncoderConfiguration.Resolution.Width
                p.resolution_H = profile.VideoEncoderConfiguration.Resolution.Height
                p.quality = profile.VideoEncoderConfiguration.Quality
                p.framerate_limit = profile.VideoEncoderConfiguration.RateControl.FrameRateLimit
                p.encoding_interval = profile.VideoEncoderConfiguration.RateControl.EncodingInterval
                p.bitrate_limit = profile.VideoEncoderConfiguration.RateControl.BitrateLimit
                self.profiles.append(p)

            for profile in self.profiles:
                self.log('getting system uri for profile ' + profile.name + " ...")
                params = mycam.devicemgmt.create_type('GetSystemUris')
                resp = mycam.media.GetStreamUri({'StreamSetup': {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}, 'ProfileToken': profile.token})
                if resp['Uri']:
                    profile.rtsp_uri = resp['Uri']
                    profile.InvalidAfterConnect = resp['InvalidAfterConnect']
                    profile.InvalidAfterReboot = resp['InvalidAfterReboot']
                    profile.Timeout = resp['Timeout']

    def choose_transport(self, rtsp_body):
        #self.log('rtsp body: ')
        #self.log(rtsp_body)
        m = re.findall(r'm=.+', rtsp_body)
        a = re.findall(r'a=.+', rtsp_body)
        m_video = [i.replace('m=', '') for i in m if 'video' in i.lower()]
        m_audio = [i.replace('m=', '') for i in m if 'audio' in i.lower()]
        print('m_video: ' + str(m_video))
        print('m_audio: ' + str(m_audio))
        for video in m_video:
            print(video.split(' '))
        chosen_video = m_video[0].split(' ')
        chosen_video_port = chosen_video[1]
        chosen_video_protocol = chosen_video[2]
        chosen_video_fmt = chosen_video[3]    
        chosen_audio = m_audio[0].split(' ')
        chosen_audio_port = chosen_audio[1]
        chosen_audio_protocol = chosen_audio[2]    
        print('chosen_video_protocol: ' + chosen_video_protocol)
        print('chosen_video_port: ' + chosen_video_port)
        print('chosen_video_fmt: ' + chosen_video_fmt)
        return ['rtp_avp_tcp']
        #print(re.findall(r'm=.+', rtsp_body))
        #print('decide between these: ' + rtsp_body())

    def rtsp_uri_ensure_username(self, uri):
        if '@' not in uri: #Simple test. Does it cover all cases?
            return uri.replace('rtsp://', 'rtsp://' + self.username + ":" + self.password + '@')

    def rtsp_connect(self, uri):
        RTSP_timeout = 10
        uri = self.rtsp_uri_ensure_username(uri)
        #uri = self.rtsp_uri#.replace('554\/11', '10554')
        self.log('opening RTSP connection to url ' + uri + ' ...')
        callback = lambda x: self.log('\n' + x) 
        sock = None
        if self.socks:
            sock = socks.socksocket() # Same API as socket.socket in the standard lib
            #The true is for remote dns resolution
            sock.set_proxy(socks.SOCKS5, self.socks_host, self.socks_port, True, self.socks_user, self.socks_password) # (socks.SOCKS5, "localhost", 1234)

        myrtsp = RTSPClient(url=uri, callback=callback, socks=sock, choose_transport=self.choose_transport)#, timeout=RTSP_timeout)
        try:
            myrtsp.do_describe()
            while myrtsp.state != 'describe':
                time.sleep(0.1)
            myrtsp.do_setup('track0')
            while myrtsp.state != 'setup':
                time.sleep(0.1)
            #Open socket to capture frames here
            myrtsp.do_play(myrtsp.cur_range, myrtsp.cur_scale)
        except Exception as e:
            print('EXCEPTION ------------------------------')
            print(e)
            myrtsp.do_teardown()
        #return camera

    def begin_stream(self):
        pass