from PyQt5.QtWidgets import QApplication,QTableWidgetItem,QFrame,QTableWidget,QWidget,QLabel
from PyQt5 import QtGui,QtCore,Qt
import sys

from Ui_AddFriends import Ui_AddFriends

class AddWin(QWidget,Ui_AddFriends):
    def __init__(self,send_sockfd,server_addr,my_id,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        #初始化属性
        self.send_sockfd = send_sockfd
        self.server_addr = server_addr
        self.my_id = my_id
        #初始化设置
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)#设置无边框
        self.label_3.hide()
        self.label_7.hide()
        self.mode = "preson"
        self.comboBox.addItems(('不限','男','女'))
        self.comboBox_2.addItems(('不限','18岁以下','18-22岁','22-30岁','30岁以上'))
        #控件触发事件
        self.Find.clicked.connect(self.find)

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

    def find(self):#查找好友
        name_or_id = self.lineEdit.text()
        if not name_or_id:
            self.lineEdit.setText("账号昵称不能为空")
            return
        gender = self.comboBox.currentText()
        age = self.comboBox_2.currentText()
        msg = '031 ' + self.my_id + ' ' + name_or_id + ' ' + gender + ' ' +age
        self.send_sockfd.sendto(msg.encode(),self.server_addr)

