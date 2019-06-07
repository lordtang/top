from PyQt5.QtWidgets import QApplication,QWidget,QMessageBox,QLabel
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from Ui_ForgetDialog import Ui_ForgetDialog
from picture_code import get_varify_image
from sendmessage import sendMessage
import sys

class Forget(QWidget, Ui_ForgetDialog):
    def __init__(self,client,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.client = client
        self.pic_code = get_varify_image()
        self.setWindowFlags(Qt.FramelessWindowHint)#设置无边框
        self.lineEdit.editingFinished.connect(self.request)
        self.lineEdit_3.editingFinished.connect(self.password_config)
        self.lineEdit_4.editingFinished.connect(self.ensure_password)
        self.pushButton_3.clicked.connect(self.resend_message)
        self.pushButton_4.clicked.connect(self.count_config)
        self.pushButton_5.clicked.connect(self.message_config)
        self.GetbackBtn.clicked.connect(self.get_back_pw)
        self.VarifyLabel = PicVarifyLabel(self)
        self.VarifyLabel.setGeometry(QtCore.QRect(460,290,150,30))
        self.VarifyLabel.setPixmap(QtGui.QPixmap("varifyCode.png"))
        self.VarifyLabel.clicked.connect(self.reget_pic_varify)
        self.GetbackBtn.hide()
        self.pushButton_3.hide()
        self.pushButton_5.hide()
        self.lineEdit_3.hide()
        self.lineEdit_4.hide()
        self.label_8.hide()
        self.label_18.hide()
        self.label_19.hide()
        self.label_5.setStyleSheet("background-color:grey")
        self.label_9.setStyleSheet('''background-color: grey;
        color: rgb(255, 255, 255);
        border-radius: 25%;''')
        self.label_15.setStyleSheet('''color:grey''')
        self.label_10.setStyleSheet("background-color:grey")
        self.label_11.setStyleSheet('''background-color: grey;
        color: rgb(255, 255, 255);
        border-radius: 25%;''')
        self.label_16.setStyleSheet('''color:grey''')
        self.label_12.setStyleSheet("background-color:grey")
        self.label_13.setStyleSheet('''background-color: grey;
        color: rgb(255, 255, 255);
        border-radius: 25%;''')
        self.label_17.setStyleSheet('''color:grey''')


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

    def request(self):
        try:
            if self.lineEdit.text():
                count = self.lineEdit.text()
                result = self.client.forget_pw_request(self.client.sockfd, count)
                config = result[1]
                self.phonenumber = result[2]
                if config == 'OK':
                    self.label_2.setStyleSheet("color:green")
                    self.label_2.setText("账号验证成功")
                elif config == 'Failed':
                    self.label_2.setStyleSheet("color:red")
                    self.label_2.setText("账号不存在")
            else:
                self.label_2.setStyleSheet("color:red")
                self.label_2.setText("账号不能为空")
        except AttributeError:
            pass
    
    def reget_pic_varify(self):
        self.pic_code = get_varify_image()
        self.VarifyLabel.setPixmap(QtGui.QPixmap("varifyCode.png"))
    
    def count_config(self):
        if self.label_2.text() == '账号验证成功' and self.label_4.text() == '':
            self.lineEdit_2.setText('')
            self.VarifyLabel.hide()
            self.lineEdit.hide()
            self.pushButton_4.hide()
            self.label_2.hide()
            self.label_5.setStyleSheet('''background-color: 
            qlineargradient(spread:pad, x1:0.0995025, y1:0.5, 
            x2:1, y2:0, stop:0 rgba(35, 201, 255, 255), 
            stop:1 rgba(255, 255, 255, 255));''')
            self.label_9.setStyleSheet('''background-color: rgb(10, 200, 255);
            color: rgb(255, 255, 255);
            border-radius: 25%;''')
            self.label_15.setStyleSheet('''color:black''')


            self.label_8.show()
            self.label_18.show()
            temp = ','.join(self.phonenumber).split(',')
            temp[3:7] = ["*","*","*","*"]
            phonenumber = ''
            for i in temp:
                phonenumber += i
            self.label_18.setText(phonenumber)
            self.label_19.show()
            self.pushButton_3.show()
            self.pushButton_5.show()
            self.message_code = sendMessage('password',self.phonenumber)
        elif self.label_2.text() != '账号验证成功':
            reply = QMessageBox.information(self,"  ","请输入正确的账号",QMessageBox.Ok)
        elif self.lineEdit_2.text != self.pic_code:
            reply = QMessageBox.information(self,"  ","验证码错误",QMessageBox.Ok)
            self.reget_pic_varify()

    def resend_message(self):
        self.message_code = sendMessage('password',self.phonenumber)

    def message_config(self):
        if self.lineEdit_2.text() == self.message_code:
            self.label_8.hide()
            self.label_18.hide()
            self.label_19.hide()
            self.lineEdit_2.hide()
            self.pushButton_3.hide()
            self.pushButton_5.hide()
            self.lineEdit_3.setGeometry(QtCore.QRect(350,230,260,30))
            self.lineEdit_3.show()
            self.lineEdit_4.setGeometry(QtCore.QRect(350,290,260,30))
            self.lineEdit_4.show()
            self.GetbackBtn.setGeometry(QtCore.QRect(350,360,260,40))
            self.GetbackBtn.show()
            self.label_4.setGeometry(QtCore.QRect(350,260,260,20))
            self.label_6.setGeometry(QtCore.QRect(350,322,260,20))
            self.label_6.show()
            self.label_10.setStyleSheet('''background-color: 
            qlineargradient(spread:pad, x1:0.0995025, y1:0.5, 
            x2:1, y2:0, stop:0 rgba(35, 201, 255, 255), 
            stop:1 rgba(255, 255, 255, 255));''')
            self.label_11.setStyleSheet('''background-color: rgb(10, 200, 255);
            color: rgb(255, 255, 255);
            border-radius: 25%;''')
            self.label_16.setStyleSheet('''color:black''')
        else:
            reply = QMessageBox.information(self,"  ","验证码错误",QMessageBox.Ok)

    def password_config(self):
        if len(self.lineEdit_3.text()) < 8 or self.lineEdit_3.text == '':
            self.label_4.setStyleSheet("color:red")
            self.label_4.setText("请输入8-16位数字、字母、字符组合")
        else:
            self.label_4.setStyleSheet("color:rgb(255,255,255)")
            self.label_4.setText('OK')

    def ensure_password(self):
        if self.lineEdit_4.text() != self.lineEdit_3.text():
            self.label_6.setStyleSheet("color:red")
            self.label_6.setText("两次输入密码不一致")
        else:
            self.label_6.setStyleSheet("color:rgb(255,255,255)")
            self.label_6.setText("OK")      

    def get_back_pw(self):
        if self.label_4.text() == 'OK' and self.label_6.text() == 'OK':
            count = self.lineEdit.text()
            newpassword = self.lineEdit_3.text()
            result = self.client.forget_pw(self.client.sockfd, count, newpassword)
            if result:
                self.label_12.setStyleSheet('''background-color: 
            qlineargradient(spread:pad, x1:0.0995025, y1:0.5, 
            x2:1, y2:0, stop:0 rgba(35, 201, 255, 255), 
            stop:1 rgba(255, 255, 255, 255));''')
                self.label_13.setStyleSheet('''background-color: rgb(10, 200, 255);
            color: rgb(255, 255, 255);
            border-radius: 25%;''')
                self.label_17.setStyleSheet('''color:black''')
                reply = QMessageBox.information(self,"  ","密码修改成功",QMessageBox.Ok)
                self.close()
            else:
                reply = QMessageBox.information(self,"  ","密码修改失败",QMessageBox.Ok)
        else:
            pass

class PicVarifyLabel(QLabel):
    clicked = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super().__init__(parent)

    def mousePressEvent(self,e):
        self.clicked.emit()