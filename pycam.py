#!/usr/bin/env python3
import threading
import sys
import socks
import time
import re
from custom_transport import *
from time import sleep
from threading import Thread
#from rx import Observable, Observer

#sys.path.insert(0, '/home/lz/Coding/python-onvif-zeep/onvif')
sys.path.insert(0, '/home/lz/Coding/python-rtsp-client')
RTSP_timeout = 10

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
host = '192.168.122.1'
port = 1080

proxies = {
    'http': 'socks5://' + user + ':' + password + '@' + host + ':' + str(port),
    'https': 'socks5://' + user + ':' + password + '@' + host + ':' + str(port)
}
#----------------------------
SocksTransport = CustomTransport(timeout=10, proxies=proxies)
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
        print('Camera ' + str(self.id) + ', ' + self.ip + ':' + self.onvif + ": " + info)    


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

#take_until(cancel_launch).\
#delay_with_selector(lambda s: Observable.timer(2**s*500))
#example_of_camera = load_cameras()[0] 
#https://repl.it/repls/SubmissiveColossalCaribou
onvif_ports = ['10080', '1080', '8080']
rtsp_ports = ['554']#, '10554']
usernames = ['admin']
passwords = ['888888', 'admin', '']
cams = [{'id': '', 'ip': '192.168.1.31', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.43', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.72', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.100', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.101', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.102', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.103', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.104', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.107', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.108', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.109', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.110', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.113', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.114', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.133', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.137', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.138', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.139', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.140', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.142', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.157', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.161', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.162', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.164', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.171', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''},
        {'id': '', 'ip': '192.168.1.173', 'onvif': '10080', 'rtsp': '554', 'username': 'admin', 'password': ''}]
#'''
cam = Camera(id = '',
             ip = '192.168.1.173',
             onvif = '8080',
             rtsp = '554',
             username = 'admin',
             password = 'admin'
             )

load_camera_information(cam)   
print("--------------------------- ONVIF SUCCESS")     
rtsp_connect(cam)
time.sleep(10)
#'''

import multiprocessing.pool
import functools

def timeout(max_timeout):
    """Timeout decorator, parameter in seconds."""
    def timeout_decorator(item):
        """Wrap the original function."""
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # raises a TimeoutError if execution exceeds max_timeout
            return async_result.get(max_timeout)
        return func_wrapper
    return timeout_decorator


f = open('results.txt', 'w')

#@timeout(5.0)
def do_camera_probe(ip, onvif_port, rtsp_port, username, password):
        try:
                #print("-------- Trying connection to " + ip + ":" + str(port))
                print("---------------------------")
                print("" + ip + ":" + str(onvif_port) + ", rtsp: " + rtsp_port + ", username: " + username + ", password: " + password)
                cam = Camera(id = '',
                             ip = ip,
                             onvif = onvif_port,
                             rtsp = rtsp_port,
                             username = username,
                             password = password
                             )

                load_camera_information(cam)   
                print("--------------------------- ONVIF SUCCESS")  
                f.write("ONVIF MATCH " + ip + ":" + str(onvif_port) + ", username: " + username + ", password: " + password + " gonna try rtsp " + rtsp_port + "\n")
                rtsp_connect(cam)
                print("--------------------------- RTSP SUCCESS")
                f.write("RTSP MATCH " + ip + ":" + str(onvif_port) + ", rtsp: " + rtsp_port + ", username: " + username + ", password: " + password + "\n")
        except Exception as e:
                #print(e)
                pass
        

cams_just_ip = [cam['ip'] for cam in cams]
#print(cams_just_ip)
threads = []
for ip in cams_just_ip:
        for onvif_port in onvif_ports:
                for rtsp_port in rtsp_ports:
                        for username in usernames:
                                for password in passwords:
                                        sleep(0.1)
                                        #do_camera_probe(obj)
                                        t = Thread(target=do_camera_probe, args=(ip,onvif_port, rtsp_port, username, password, ))
                                        t.start()
                                        threads.append(t)
print("---------------------------------------JOINING THREADS")
for thread in threads:
        thread.join()
f.close()
'''
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
'''
