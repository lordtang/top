from PyQt5.QtWidgets import QApplication,QTableWidgetItem,QFrame,QTableWidget,QWidget
from PyQt5 import QtGui,QtCore,Qt
import sys
import threading
import socket
import time
import os
from datetime import datetime
from ctypes import windll

from Ui_VoiceChatWin import Ui_VoiceChatWin
from media import AudioServer,AudioClient

class VoiceChatWin(QWidget,Ui_VoiceChatWin):
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
        self.Micro_volume_Slider.hide()
        self.Speaker_volume_Slider.hide()
        self.setGeometry(location[0],location[1],270,700)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)#设置无边框
        self.is_mute = False #判断是否静音的变量
        self.forewin_volume_set() #初始化窗口的音量
        self.audio_chat_staus = False
        #初始化按钮设置
        self.Micro.setEnabled(False)
        self.Volume.setEnabled(False)
        self.Video.setEnabled(False)
        #按钮触发事件
        self.Micro.clicked.connect(self.show_micro_volume_slider)
        self.Micro_volume_Slider.valueChanged.connect(self.start_adjust_micro_volume)
        self.Volume.clicked.connect(self.show_speaker_volume_slider)
        self.Speaker_volume_Slider.valueChanged.connect(self.start_adjust_speaker_volume)
        #不同模式下新建窗口的设置
        if mode == "request":
            #发起方的按钮初始化
            self.Answer.hide()
            self.Hang_up.clicked.connect(self.interupt_chat)
            self.Close.clicked.connect(self.interupt_chat)
        else:
            #接收方的按钮初始化
            self.Hang_up.hide()
            self.Answer.clicked.connect(self.agree_chat)
            self.Hang_up.clicked.connect(self.interupt_chat)
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
        self.micro_volume = 24
        self.speaker_volume = 24

    def show_micro_volume_slider(self):#打开关闭麦克风音量调节器
        if self.Micro_volume_Slider.isVisible() == True:
            self.Micro_volume_Slider.hide()
        else:
            self.Micro_volume_Slider.show()

    def start_adjust_micro_volume(self):#打开麦克风音量调节线程
        th = threading.Thread(target=self.adjust_micro_volume)
        th.setDaemon(True)
        th.start()

    def adjust_micro_volume(self):#调节麦克风音量
        if self.Micro_volume_Slider.value()%2 == 0:
            Volume = self.Micro_volume_Slider.value()
        else:
            Volume = (self.Micro_volume_Slider.value()-1)
        print(Volume)
        WM_APPCOMMAND = 0x0319
        APPCOMMAND_MICROPHONE_VOLUME_DOWN = 25 #减小麦克风音量
        APPCOMMAND_MICROPHONE_VOLUME_UP = 26 #增加麦克风音量
        hwnd = windll.user32.GetForegroundWindow()
        if Volume > self.micro_volume:
            while Volume > self.micro_volume:
                windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_MICROPHONE_VOLUME_UP*0x10000)
                self.micro_volume += 2
        elif Volume < self.micro_volume:
            while Volume < self.micro_volume:
                windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_MICROPHONE_VOLUME_DOWN*0x10000)
                self.micro_volume -= 2
        else:
            pass
        print(self.micro_volume)
        if self.micro_volume == 0:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("images/05-09.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Micro.setIcon(icon)
            self.Micro.setIconSize(QtCore.QSize(32, 32))
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("images/05-02.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Micro.setIcon(icon)
            self.Micro.setIconSize(QtCore.QSize(32, 32))

    def show_speaker_volume_slider(self):#打开关闭扬声器音量调节器
        if self.Speaker_volume_Slider.isVisible() == True:
            self.Speaker_volume_Slider.hide()
        else:
            self.Speaker_volume_Slider.show()

    def start_adjust_speaker_volume(self):#打开扬声器音量调节线程
        th = threading.Thread(target=self.adjust_speaker_volume)
        th.setDaemon(True)
        th.start()

    def adjust_speaker_volume(self):#调节扬声器音量
        if self.Speaker_volume_Slider.value()%2 == 0:
            Volume = self.Speaker_volume_Slider.value()
        else:
            Volume = (self.Speaker_volume_Slider.value()-1)
        print(Volume)
        WM_APPCOMMAND = 0x0319
        APPCOMMAND_VOLUME_UP = 10
        APPCOMMAND_VOLUME_DOWN = 9
        hwnd = windll.user32.GetForegroundWindow()
        if Volume > self.speaker_volume:
            while Volume > self.speaker_volume:
                windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_VOLUME_UP*0x10000)
                self.speaker_volume += 2
        elif Volume < self.speaker_volume:
            while Volume < self.speaker_volume:
                windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_VOLUME_DOWN*0x10000)
                self.speaker_volume -= 2
        else:
            pass
        print(self.speaker_volume)
        if self.speaker_volume == 0:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("images/05-03.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Volume.setIcon(icon)
            self.Volume.setIconSize(QtCore.QSize(32, 32))
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("images/05-08.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.Volume.setIcon(icon)
            self.Volume.setIconSize(QtCore.QSize(32, 32))

    def agree_chat(self):#接受语音聊天请求
        self.audio_chat_staus = True
        self.rsp_voice_server = AudioServer(10088,4)
        self.rsp_voice_client = AudioClient(self.c_server_addr[0],self.c_server_addr[1],4)
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        #发送接受语音消息
        msg = '0661 ' + self.friend_id + ' ' + self.my_id + ' ' + ip + ' ' + '10088'
        print("server_addr:",self.server_addr)
        self.send_sockfd.sendto(msg.encode(),self.server_addr)
        #设置按钮
        self.Micro.setEnabled(True)
        self.Volume.setEnabled(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/05-08.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Volume.setIcon(icon)
        self.Volume.setIconSize(QtCore.QSize(32, 32))
        self.Answer.hide()
        self.Hang_up.show()
        #开启线程计时
        th = threading.Thread(target=self.count_time,args=(self.label_3,))
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

    def interupt_chat(self):#终止语音聊天
        self.close()
        self.kill_thread = True
        #发送终止视频信息
        msg = '0662 ' + self.my_id + ' ' + self.friend_id + ' ' + self.mode
        self.send_sockfd.sendto(msg.encode(),self.server_addr)
        if self.mode == 'request':#处理请求方
            #在消息文件中添加一条消息
            time_tamp = str(datetime.now())
            msg = '036 ' + self.my_id + ' ' + self.friend_id + ' ' + '语音通话: %s'%self.label_3.text() + ' ' + time_tamp + '\n'
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
            self.label_3.setText('Null')
            if self.audio_chat_staus:#如果正在通话
                try:    
                    del self.req_voice_server
                except:
                    pass
                try:    
                    del self.req_voice_client
                except:
                    pass
            else:#如果没有通话
                try:
                    del self.req_voice_server
                except:
                    pass
                try:
                    del self.req_voice_client
                except:
                    pass
        else:#处理接收方
            #在消息文件中添加一条消息
            time_tamp = str(datetime.now())
            msg = '063 ' + self.friend_id + ' ' + self.my_id + ' ' + '语音通话: %s'%self.label_3.text() + ' ' + time_tamp + '\n'
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
            self.label_3.setText('Null')
            if self.audio_chat_staus:#如果正在通话
                try:
                    del self.rsp_voice_server
                except:
                    pass
                try:
                    del self.rsp_voice_client
                except:
                    pass
            else:#如果没有通话
                pass

