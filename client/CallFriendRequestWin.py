from PyQt5.QtWidgets import QApplication,QTableWidgetItem,QFrame,QTableWidget,QWidget,QLabel
from PyQt5 import QtGui,QtCore,Qt
import sys

from Ui_FriendRequestWin import Ui_Form

class FrirenRequestWin(QWidget,Ui_Form):
    def __init__(self,my_id,friend_id,friends_info,reshow_friends_list_signal,send_sockfd,server_addr,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.my_id = my_id
        self.friend_id = friend_id
        self.friends_info = friends_info
        text = "用户:%s请求加您为好友"%friend_id
        self.label_2.setText(text)
        self.send_sockfd = send_sockfd
        self.server_addr = server_addr
        self.reshow_friends_list_signal = reshow_friends_list_signal
        self.pushButton.clicked.connect(self.agree)
        self.pushButton_2.clicked.connect(self.refuse)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)#设置无边框



    def agree(self):#同意添加好友请求
        print("同意加好友：",self.friend_id,self.my_id)
        msg = '0311 ' + self.friend_id + ' ' + self.my_id
        self.send_sockfd.sendto(msg.encode(),self.server_addr)
        self.friends_info[self.friend_id] = ''
        if self.reshow_friends_list_signal.text() == '2':
            self.reshow_friends_list_signal.setText('1')
        else:
            self.reshow_friends_list_signal.setText('2')
        self.close()

    def refuse(self):#拒绝加好友请求
        self.close()
