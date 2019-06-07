from socket import *
from PyQt5.QtGui import QImage,QPixmap
from PyQt5 import Qt
import threading
import cv2
import re
import time
import sys
import os
import struct
import pickle
import zlib
import wave


class Video_Client(threading.Thread):
    def __init__(self ,ip, port, label,version, level):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ADDR = (ip, port)
        self.label = label
        if level <= 3:
            self.interval = level
        else:
            self.interval = 3
        self.fx = 1 / (self.interval + 1)
        if self.fx < 0.3:
            self.fx = 0.3
        if version == 4:
            self.sock = socket(AF_INET, SOCK_STREAM)
        else:
            self.sock = socket(AF_INET6, SOCK_STREAM)
        self.cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)
        self.stop_vclient = []
    def __del__(self):
        self.sock.close()
        self.cap.release()
        print("视频关闭")
    def run(self):
        print("VEDIO client starts...")
        while True:
            try:
                self.sock.connect(self.ADDR)
                break
            except:
                continue
        print("VEDIO client connected...")
        while self.cap.isOpened():
            try:
                if self.stop_vclient[0] == 'True':
                    self.__del__()
                    break
            except:
                pass
            try:
                ret, frame = self.cap.read()
                sframe = cv2.resize(frame, (0,0), fx=self.fx, fy=self.fx)
                sframe = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                data = pickle.dumps(sframe)
                zdata = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
                try:
                    self.sock.sendall(struct.pack("L", len(zdata)) + zdata)
                except Exception:
                    break
                frame = cv2.resize(frame,(240,180))
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                Pixmap = QPixmap.fromImage(img)
                self.label.setAlignment(Qt.Qt.AlignCenter)
                self.label.setPixmap(Pixmap)
                for i in range(self.interval):
                    self.cap.read()
            except:
                continue


# 服务器端最终代码如下，增加了对接收到数据的解压缩处理。
class Video_Server(threading.Thread):
    def __init__(self, port, label, version) :
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.label = label
        self.ADDR = ('0.0.0.0', port)
        if version == 4:
            self.sock = socket(AF_INET ,SOCK_STREAM)
            self.sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        else:
            self.sock = socket(AF_INET6 ,SOCK_STREAM)
        self.stop_vserver = []
    def __del__(self):
        self.sock.close()
        try:
            cv2.destroyAllWindows()
        except:
            pass
        print("视频服务停止")
    def run(self):
        print("VEDIO server starts...")
        self.sock.bind(self.ADDR)
        self.sock.settimeout(30)
        print(self.ADDR,"正在监听...")
        self.sock.listen(1)
        conn = ''
        try:
            conn, addr = self.sock.accept()
        except:
            pass
        if conn:
            print("remote VEDIO client success connected...")
            data = "".encode("utf-8")
            payload_size = struct.calcsize("L")
            try:
                while True:
                    print('stop_server:',self.stop_vserver)
                    try:
                        if self.stop_vserver[0] == 'True':
                            self.__del__()
                            break
                    except:
                        pass
                    try:
                        while len(data) < payload_size:
                            data += conn.recv(81920)
                        packed_size = data[:payload_size]
                        data = data[payload_size:]
                        msg_size = struct.unpack("L", packed_size)[0]
                        while len(data) < msg_size:
                            data += conn.recv(81920)
                        zframe_data = data[:msg_size]
                        data = data[msg_size:]
                        frame_data = zlib.decompress(zframe_data)
                        frame = pickle.loads(frame_data)
                        frame = cv2.resize(frame,(1400,1050))
                        img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                        Pixmap = QPixmap.fromImage(img)
                        self.label.setAlignment(Qt.Qt.AlignCenter)
                        self.label.setPixmap(Pixmap)

                        if cv2.waitKey(1) & 0xFF == 27:
                            break
                    except:
                        continue
            except Exception:
                print("视频连接中断")
        else:
            pass