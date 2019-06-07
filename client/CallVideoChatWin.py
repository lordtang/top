import cv2
import threading
from PyQt5.QtWidgets import QApplication,QTableWidgetItem,QFrame,QTableWidget,QWidget
from PyQt5 import QtGui,QtCore,Qt
from PyQt5.QtGui import QImage,QPixmap
import sys
import socket
import time
import os
from datetime import datetime
from ctypes import windll

from Ui_VideoChatWin import Ui_VideoChatWin
from media import VideoServer,VideoClient

class VideoChatWin(QWidget,Ui_VideoChatWin):
    def __init__(self,location,mode,send_sockfd=None,my_id=None,friend_id=None,c_server_addr=None,server_addr=None,reshow_signal=None,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.mode = mode
        self.send_sockfd = send_sockfd
        self.my_id = my_id
        self.friend_id = friend_id
        self.c_server_addr = c_server_addr
        self.server_addr = server_addr
        self.reshow_signal = reshow_signal
        self.setGeometry(location[0],location[1],430,760)
        self.Volume_slider.hide()
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)#设置无边框
        self.is_mute = False #判断是否静音的变量
        self.forewin_volume_set() #初始化窗口音量
        self.video_chat_staus = False
        print("新建视频聊天窗口成功")
        #按钮触发事件
        self.Volume.clicked.connect(self.show_volume_slider)
        self.Volume_slider.valueChanged.connect(self.start_adjust_volume)
        self.Mute.clicked.connect(self.mute)
        #不同模式新建窗口设置
        if self.mode == "request":
            self.show_my_image()
            self.Mute.setEnabled(False)
            self.Switch.setEnabled(False)
            self.Volume.setEnabled(False)
            self.Answer.hide()
            self.label.setText("等待接听")
            self.HangUp.move(190,660)
            self.HangUp.clicked.connect(self.interupt_chat)
            self.Close.clicked.connect(self.interupt_chat)
            self.kill_thread = False
        else:
            self.Mute.setEnabled(False)
            self.Switch.setEnabled(False)
            self.Volume.setEnabled(False)
            self.Answer.clicked.connect(self.agree_chat)
            self.HangUp.clicked.connect(self.interupt_chat)
            self.Close.clicked.connect(self.interupt_chat)

    def mousePressEvent(self, event):
        if event.button()==Qt.Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
        try:
            if self.expression_form.isVisible():
                self.expression_form.hide()
        except Exception:
            pass

    def mouseMoveEvent(self, QMouseEvent):
        try:
            if Qt.Qt.LeftButton and self.m_flag:  
                self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
                QMouseEvent.accept()
        except AttributeError:
            pass
    
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False

    def show_volume_slider(self):#打开关闭音量调节器
        if self.Volume_slider.isVisible() == True:
            self.Volume_slider.hide()
        else:
            self.Volume_slider.show()

    def start_adjust_volume(self):#打开音量调节线程
        th = threading.Thread(target=self.adjust_volume)
        th.setDaemon(True)
        th.start()

    def forewin_volume_set(self):#设置当前窗口音量
        WM_APPCOMMAND = 0x0319
        APPCOMMAND_VOLUME_UP = 0x0a
        APPCOMMAND_VOLUME_DOWN = 0x09
        APPCOMMAND_MICROPHONE_VOLUME_DOWN = 25 #减小麦克风音量
        APPCOMMAND_MICROPHONE_VOLUME_UP = 26 #增加麦克风音量
        hwnd = windll.user32.GetForegroundWindow()
        for i in range(51):
            windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_VOLUME_DOWN*0x10000)
            windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_MICROPHONE_VOLUME_DOWN*0x10000)
        #设置初始音量为24
        for i in range(12):
            windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_VOLUME_UP*0x10000)
            windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_MICROPHONE_VOLUME_UP*0x10000)
        self.volume = 24

    def adjust_volume(self):#调节音量
        if self.Volume_slider.value()%2 == 0:
            Volume = self.Volume_slider.value()
        else:
            Volume = (self.Volume_slider.value()-1)
        print(Volume)
        WM_APPCOMMAND = 0x0319
        APPCOMMAND_VOLUME_UP = 10
        APPCOMMAND_VOLUME_DOWN = 9
        APPCOMMAND_MICROPHONE_VOLUME_DOWN = 25 #减小麦克风音量
        APPCOMMAND_MICROPHONE_VOLUME_UP = 26 #增加麦克风音量
        hwnd = windll.user32.GetForegroundWindow()
        if Volume > self.volume:
            while Volume > self.volume:
                windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_VOLUME_UP*0x10000)
                windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_MICROPHONE_VOLUME_UP*0x10000)
                self.volume += 2
        elif Volume < self.volume:
            while Volume < self.volume:
                windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_VOLUME_DOWN*0x10000)
                windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_MICROPHONE_VOLUME_DOWN*0x10000)
                self.volume -= 2
        else:
            pass
        print(self.volume)

    def mute(self):#静音开关
        WM_APPCOMMAND = 0x319
        APPCOMMAND_MICROPHONE_VOLUME_MUTE = 24 #麦克风静音
        APPCOMMAND_MIC_ON_OFF_TOGGLE = 44 #麦克风开关
        hwnd = windll.user32.GetForegroundWindow()
        if self.is_mute:
            self.is_mute = False
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("images/06-03.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Mute.setIcon(icon)
            self.Mute.setIconSize(QtCore.QSize(30, 30))
            windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_MICROPHONE_VOLUME_MUTE*0x10000)
        else:
            self.is_mute = True
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("images/06-11.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Mute.setIcon(icon)
            self.Mute.setIconSize(QtCore.QSize(30, 30))
            windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_MICROPHONE_VOLUME_MUTE*0x10000)

    def show_my_image(self):
        self.cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)
        th = threading.Thread(target=self.display_my_image)
        th.setDaemon(True)
        th.start()

    def display_my_image(self):
        self.kill_thread = False
        while self.cap.isOpened():
            if self.kill_thread:
                break
            if self.video_chat_staus:
                break
            else:
                success, frame = self.cap.read()
                # RGB转BGR
                frame = cv2.resize(frame,(1400,1050))
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                Pixmap = QPixmap.fromImage(img)
                self.FriendVideoLabel.setAlignment(Qt.Qt.AlignCenter)
                self.FriendVideoLabel.setPixmap(Pixmap)
                cv2.waitKey(1)

    def agree_chat(self):#接受视频聊天请求
        self.video_chat_staus = True
        self.rsp_video_server = VideoServer(10086,self.FriendVideoLabel)
        self.rsp_video_client = VideoClient(self.c_server_addr[0],self.c_server_addr[1],self.MyVideoLabel)
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        #发送接受视频消息
        msg = '0671 ' + self.friend_id + ' ' + self.my_id + ' ' + ip + ' ' + '10086'
        self.send_sockfd.sendto(msg.encode(),self.server_addr)
        #关闭头像显示框
        self.HeadPic.hide()
        #设置按钮
        self.Mute.setEnabled(True)
        self.Switch.setEnabled(True)
        self.Volume.setEnabled(True)
        self.Answer.hide()
        self.HangUp.move(190,660)
        #开启线程计时
        th = threading.Thread(target=self.count_time,args=(self.label,))
        th.setDaemon(True)
        th.start()

    def count_time(self,label):#计时函数
        s1 = 0
        s2 = 0
        m1 = 0
        m2 = 0
        while True:
            if label.text() == 'Null':
                print("计时终止")
                break
            if s1 == 10:
                s1 = 0
                s2 += 1
            if s2 == 6:
                s2 = 0
                m1 += 1
            if m1 == 10:
                m1 = 0
                m2 += 1
            count = str(m2)+str(m1)+':'+str(s2)+str(s1)
            label.setText(count)
            time.sleep(1)
            s1 += 1

    def interupt_chat(self):
        try:
            self.cap.release()
        except AttributeError:
            pass
        self.close()
        self.kill_thread = True
        #发送终止视频信息
        msg = '0672 ' + self.my_id + ' ' + self.friend_id + ' ' + self.mode
        self.send_sockfd.sendto(msg.encode(),self.server_addr)
        if self.mode == 'request':#处理请求方
            #在消息文件中添加一条消息
            time_tamp = str(datetime.now())
            msg = '036 ' + self.my_id + ' ' + self.friend_id + ' ' + '视频通话: %s'%self.label.text() + ' ' + time_tamp + '\n'
            path = 'Top files\\%s\\message_record.txt'%self.my_id
            try:
                with open(path,'a') as f:
                    f.write(msg)
                f.close()
            except:
                pass
            if self.reshow_signal.text() == '1':
                self.reshow_signal.setText('2')
            else:
                self.reshow_signal.setText('1')
            self.label.setText('Null')
            if self.video_chat_staus:#如果正在通话
                try:    
                    del self.req_video_server
                    print("关闭请求方视频服务")
                except:
                    pass
                try:    
                    del self.req_video_client
                    print("关闭请求方视频客户端")
                except:
                    pass
            else:#如果没有通话
                try:
                    del self.req_video_server
                    print("关闭请求方视频服务")
                except:
                    pass
                try:
                    del self.req_video_client
                    print("关闭请求方视频客户端")
                except:
                    pass
        else:#处理接收方
            #在消息文件中添加一条消息
            time_tamp = str(datetime.now())
            msg = '063 ' + self.friend_id + ' ' + self.my_id + ' ' + '视频通话: %s'%self.label.text() + ' ' + time_tamp + '\n'
            path = 'Top files\\%s\\message_record.txt'%self.my_id
            try:
                with open(path,'a') as f:
                    f.write(msg)
                f.close()
            except:
                pass
            if self.reshow_signal.text() == '1':
                self.reshow_signal.setText('2')
            else:
                self.reshow_signal.setText('1')
            self.label.setText('Null')
            if self.video_chat_staus:#如果正在通话
                try:
                    del self.rsp_video_server
                    print("关闭接收方视频服务")
                except:
                    pass
                try:
                    del self.rsp_video_client
                    print("关闭接收方视频客户端")
                except:
                    pass
            else:#如果没有通话
                try:
                    del self.rsp_video_server
                    print("关闭接收方视频服务")
                except:
                    pass
                try:
                    del self.rsp_video_client
                    print("关闭接收方视频客户端")
                except:
                    pass

