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
        print('Camera ' + str(self.id) + ', ' + self.ip + ':' + self.onvif + ": " + info)    


    def probe_information(camera):
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
        print(resp)
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

    def callback(s):
        #print(s)
        pass

    def rtsp_connect(camera):
        url = camera.rtsp_uri#.replace('554\/11', '10554')
        camera.log('opening RTSP connection to url ' + url + ' ...')

        s = socks.socksocket() # Same API as socket.socket in the standard lib
        s.set_proxy(socks.SOCKS5, "localhost") # (socks.SOCKS5, "localhost", 1234)

        myrtsp = RTSPClient(url=url,callback=callback, socks=s, process_describe_response=decide_streaming, timeout=RTSP_timeout)
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