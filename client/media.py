import sys
import time
import cv2
import re
import pyaudio
import pickle
import os
import struct
import zlib
import wave
from vchat import Video_Server, Video_Client
from achat import Audio_Server, Audio_Client

class VideoServer():
    def __init__(self,port,label,version=4):
        '''
        port：服务绑定端口号
        label:视频显示控件
        version：IPV4或IPV6
        '''
        self.vserver = Video_Server(port, label, version)
        self.stop_vserver = self.vserver.stop_vserver
        self.aserver = Audio_Server(port+1, version)
        self.stop_aserver = self.aserver.stop_aserver
        self.vserver.start()
        self.aserver.start()

    def __del__(self):
        print('media的del函数触发')
        self.stop_vserver.append('True')
        self.stop_aserver.append('True')
        time.sleep(0.05)

class VideoClient():
    def __init__(self,ip,port,label,version=4,level=1):
        '''
        ip:接收端的IP地址
        port:接收的端口号
        version:协议版本号
        level:视频流抽帧频率
        '''
        self.vclient = Video_Client(ip, port, label, version, level)
        self.stop_vclient = self.vclient.stop_vclient
        self.aclient = Audio_Client(ip, port+1, version)
        self.stop_aclient = self.aclient.stop_aclient

        self.vclient.start()
        self.aclient.start()

    def __del__(self):
        print('media的del函数触发')
        self.stop_vclient.append('True')
        self.stop_aclient.append('True')

class AudioServer():
    def __init__(self,port,version=4):
        '''
        port：服务绑定端口号
        label:视频显示控件
        version：IPV4或IPV6
        '''
        self.aserver = Audio_Server(port, version)
        self.stop_aserver = self.aserver.stop_aserver
        self.aserver.start()

    def __del__(self):
        print('media的del函数触发')
        self.stop_aserver.append('True')

class AudioClient():
    def __init__(self,ip,port,version=4):
        '''
        ip:接收端的IP地址
        port:接收的端口号
        version:协议版本号
        level:视频流抽帧频率
        '''
        self.aclient = Audio_Client(ip, port, version)
        self.stop_aclient = self.aclient.stop_aclient
        self.aclient.start()

    def __del__(self):
        print('media的del函数触发')
        self.stop_aclient.append('True')
        