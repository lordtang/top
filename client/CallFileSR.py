from PyQt5.QtWidgets import QApplication,QTableWidgetItem,QFrame,QTableWidget,QWidget,QLabel
from PyQt5 import QtGui,QtCore,Qt
import sys

from Ui_FileSR import Ui_FileSendRecv

class FileSRWin(QWidget,Ui_FileSendRecv):
    def __init__(self,location,icon_path,filename,file_size,mode,parent=None):
        super().__init__(parent)
        self.mode = mode
        if file_size/(1024**2) > 1:
            self.filesize = '(' + str(round(file_size/(1024**2),2)) + ' MB)'
        else:
            self.filesize = '(' + str(round(file_size/(1024),2)) + ' KB)'
        # if self.mode == 'send':
        #     self.RecvButton.hide()
        self.setupUi(self)
        self.setGeometry(location[0],location[1],350,700)
        self.setWindowFlags(Qt.Qt.FramelessWindowHint)#设置无边框
        self.CancelButton.clicked.connect(self.close)
        self.IconLabel.setPixmap(QtGui.QPixmap(icon_path))
        self.FilenameLabel.setText(filename+self.filesize)
        self.interupt_flag = QLabel()
        self.interupt_flag.setText('False')
        self.interupt_flag.hide()

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