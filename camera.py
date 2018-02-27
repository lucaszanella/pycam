import sys
#sys.path.insert(0, '/home/lz/Coding/python-onvif-zeep/onvif')
sys.path.insert(0, '/home/deps/python-rtsp-client')
sys.path.insert(0, '/home/deps/python-native-nmap')
sys.path.insert(0, '/home/deps/PySocks')

from custom_transport import *
#from client import *
from rtsp import RTSPClient
import socks

class Camera():
    def __init__(self, id=None, ip=None, onvif=None, rtsp=None, username=None, password=None, socks=None):
        self.id = id
        self.ip = ip
        self.onvif = onvif
        self.rtsp = rtsp
        self.username = username
        self.password = password
        self.rtsp_uri = None

        if socks:
            self.socks = True
            self.socks_user = socks.user or ''
            self.socks_password = socks.password or ''
            self.socks_host = socks.host or 'localhost'
            self.socks_port = socks.port or 1080

            proxies = {
                'http': 'socks5://' + self.socks_user + ':' + self.socks_password + '@' + self.socks_host + ':' + str(self.socks_port),
                'https': 'socks5://' + self.socks_user + ':' + self.socks_password + '@' + self.socks_host + ':' + str(self.socks_port)
            }

            self.socks_transport = CustomTransport(timeout=10, proxies=proxies)
        
    def log(self, info):
        print('Camera ' + str(self.id) + ', ' + self.ip + ':' + self.onvif + ": " + info)

    def probe_information(self):
        self.log('loading information...')
        wsdl = '/home/deps/python-onvif-zeep/wsdl'
        mycam = ONVIFCamera(self.ip, 
                            self.onvif,
                            self.username, 
                            self.password,
                            wsdl, 
                            transport=self.socks_transport)
        self.log('getting capabilities...')
        resp = mycam.devicemgmt.GetCapabilities()
        #self.log(resp)
        if resp["Imaging"]:
            self.log('supports imaging services')
            imaging_url = resp["Imaging"]["XAddr"]
        if resp["Media"]:
            self.log('supports media services')
            self.log('querying media services...')
            media_service = mycam.create_media_service()
            self.log('querying profiles...')
            profiles = media_service.GetProfiles()
            # Use the first profile and Profiles have at least one
            token = profiles[0].token
            self.log('getting system uri...')
            params = mycam.devicemgmt.create_type('GetSystemUris')
            resp = mycam.media.GetStreamUri({'StreamSetup':{'Stream':'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}, 'ProfileToken':token})
            #print(resp)
            #self.rtsp_uri = resp["Uri"]
        #return camera

    def decide_streaming(self, rtsp_body):
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
        #print(re.findall(r'm=.+', rtsp_body))
        #print('decide between these: ' + rtsp_body())

    def rtsp_connect(self):
        RTSP_timeout = 10
        url = self.rtsp_uri#.replace('554\/11', '10554')
        self.log('opening RTSP connection to url ' + url + ' ...')

        sock = None
        if self.socks:
            sock = socks.socksocket() # Same API as socket.socket in the standard lib
            sock.set_proxy(socks.SOCKS5, "localhost") # (socks.SOCKS5, "localhost", 1234)

        myrtsp = RTSPClient(url=url,callback=callback, socks=sock, process_describe_response=decide_streaming, timeout=RTSP_timeout)
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

    def begin_stream(self):
        pass