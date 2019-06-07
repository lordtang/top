from PyQt5.QtWidgets import QWidget,QFrame,QLabel,QPushButton,QMessageBox
from PyQt5 import QtGui,QtCore,Qt
import time
import os

class Friend_info_item(QFrame):
    def __init__(self,friends_info,my_id,aim_id,nick_name,age,gender,pic_byte,send_sockfd,server_addr,parent=None):
        super().__init__(parent)
        self.send_sockfd = send_sockfd
        self.server_addr = server_addr
        self.setStyleSheet("border:0.5px solid grey;")
        self.friends_info = friends_info
        self.my_id = my_id
        self.aim_id = aim_id
        self.resize(200,100)
        self.head_pic_label = QLabel(self)
        filename = aim_id+'.jpg'
        f = open('temp_info/head_pic/'+filename,'wb')
        f.write(pic_byte)
        f.close()
        path = 'temp_info/head_pic/%s'%filename
        self.head_pic_label.setPixmap(QtGui.QPixmap(path))
        self.head_pic_label.resize(80,80)
        self.setStyleSheet('border:0px;')
        self.head_pic_label.setScaledContents(True)
        self.head_pic_label.move(5,10)
        self.nick_name_label = QLabel(self)
        self.nick_name_label.setText(nick_name)
        self.nick_name_label.setStyleSheet("border:0px;")
        self.nick_name_label.resize(100,20)
        self.nick_name_label.move(90,20)
        self.id_label = QLabel(self)
        self.id_label.setText(self.aim_id)
        self.id_label.setStyleSheet('border:0px;')
        self.id_label.hide()
        self.age_label = QLabel(self)
        self.age_label.setText(age)
        self.age_label.setStyleSheet("border:0px;")
        self.age_label.resize(25,25)
        self.age_label.move(90,55)
        self.gender_label = QLabel(self)
        if gender == '男':
            self.gender_label.setPixmap(QtGui.QPixmap('images/08-01.png'))
        elif gender == '女':
            self.gender_label.setPixmap(QtGui.QPixmap('images/08-02.png'))
        self.gender_label.resize(20,20)
        self.gender_label.setStyleSheet("border:0px;")
        self.gender_label.setScaledContents(True)
        self.gender_label.move(115,60)
        self.add_btn = QPushButton(self)
        self.add_btn.setStyleSheet("border-radius:3px;background-color:#009BDB;color:white;")
        self.add_btn.setText('加好友')
        self.add_btn.resize(50,20)
        self.add_btn.setCursor(Qt.QCursor(Qt.Qt.PointingHandCursor))
        self.add_btn.move(150,60)
        #触发事件
        self.add_btn.clicked.connect(self.request_add_friend)

    def request_add_friend(self):
        if self.aim_id in self.friends_info:
            reply = Qt.QMessageBox.information(self,'提示','该用户已经是您的好友',Qt.QMessageBox.Yes)
            return
        msg = '0310 ' + self.my_id + ' ' + self.aim_id
        self.send_sockfd.sendto(msg.encode(),self.server_addr)
        reply = Qt.QMessageBox.information(self,'提示','发送好友请求成功',Qt.QMessageBox.Yes)
