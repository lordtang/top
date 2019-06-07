from socket import *
import threading
import cv2
import re
import sys
import os
import time
import pyaudio
import struct
import pickle
import zlib
import wave


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 0.1
WAVE_OUTPUT_FILENAME = "output.wav"



class Audio_Server(threading.Thread):
    def __init__(self, port, version) :
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR = ('0.0.0.0', port)
        if version == 4:
            self.sock = socket(AF_INET ,SOCK_STREAM)
            self.sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        else:
            self.sock = socket(AF_INET6 ,SOCK_STREAM)
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.stop_aserver = []
    def __del__(self):
        self.sock.close()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()

    def run(self):
        print("AUDIO server starts...")
        self.sock.bind(self.ADDR)
        self.sock.settimeout(30)
        self.sock.listen(1)
        print(self.ADDR,'正在监听...')
        while True:
            conn = ''
            try:
                conn, addr = self.sock.accept()
            except:
                pass
            if conn:
                print("remote AUDIO client success connected...")
                data = "".encode("utf-8")
                payload_size = struct.calcsize("L")
                self.stream = self.p.open(format=FORMAT,
                                        channels=CHANNELS,
                                        rate=RATE,
                                        output=True,
                                        frames_per_buffer = CHUNK
                                        )
                while True:
                    if self.stop_aserver:
                        print("音频服务停止")
                        self.__del__()
                        return
                    try:
                        while len(data) < payload_size:
                            data += conn.recv(81920)
                        packed_size = data[:payload_size]
                        data = data[payload_size:]
                        msg_size = struct.unpack("L", packed_size)[0]
                        while len(data) < msg_size:
                            data += conn.recv(81920)
                        frame_data = data[:msg_size]
                        data = data[msg_size:]
                        frames = pickle.loads(frame_data)
                        for frame in frames:
                            self.stream.write(frame, CHUNK)
                    except Exception:
                        print("音频连接中断")
            else:
                pass

class Audio_Client(threading.Thread):
    def __init__(self ,ip, port, version):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR = (ip, port)
        if version == 4:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6, SOCK_STREAM)
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.stop_aclient = []
    def __del__(self) :
        self.sock.close()
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
    def run(self):
        print("AUDIO client starts...")
        while True:
            try:
                self.sock.connect(self.ADDR)
                print("连接到:",self.ADDR)
                break
            except:
                continue
        print("AUDIO client connected...")
        self.stream = self.p.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK)
        while self.stream.is_active():
            if self.stop_aclient:
                print("音频关闭")
                self.__del__()
                break
            frames = []
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = self.stream.read(CHUNK)
                frames.append(data)
            senddata = pickle.dumps(frames)
            try:
                self.sock.sendall(struct.pack("L", len(senddata)) + senddata)
            except:
                break
