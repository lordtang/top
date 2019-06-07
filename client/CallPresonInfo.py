import sys
from PyQt5.QtWidgets import QApplication,QWidget
from PyQt5.QtCore import Qt
from PyQt5 import QtGui,QtCore
from socket import socket
import time

from Ui_PersonInfo import Ui_PresonInfo

class PersonInfo(QWidget,Ui_PresonInfo):
    def __init__(self,info=[],parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)#设置无边框
        self.label_2.setPixmap(QtGui.QPixmap(info[5]))
        self.label_3.setText(info[1])
        self.label_9.setText(info[0])
        if info[4] == '0':
            self.label_10.setText('男')
        elif info[4] == '1':
            self.label_10.setText('女')
        self.label_11.setText(info[3])
        self.label_12.setText(info[2])

    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            
    def mouseMoveEvent(self, QMouseEvent):
        try:
            if Qt.LeftButton and self.m_flag:  
                self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
                QMouseEvent.accept()
        except AttributeError:
            pass