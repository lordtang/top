from PyQt5.QtWidgets import QApplication,QWidget,QMessageBox
from PyQt5.QtCore import Qt,QRegExp
# from PyQt5.QtGui import QIntValidator,QRegExpValidator
from Ui_RegisterDialog import Ui_Dialog
import zhenzismsclient as smsclient
import random
import sys

from sendmessage import sendMessage

class Register(QWidget, Ui_Dialog):
    def __init__(self,client,parent=None):
        self.client = client
        super().__init__(parent)
        self.setupUi(self)
        self.isalive = True
        self.setWindowFlags(Qt.FramelessWindowHint)#设置无边框
        self.usernameLe.editingFinished.connect(self.request)
        self.passwordLe.editingFinished.connect(self.checkpassword)
        self.ensureLe.editingFinished.connect(self.ensurepassword)
        self.RegisterBtn.clicked.connect(self.regest)
        self.pushButton_3.clicked.connect(self.send_message)
        self.pushButton_4.clicked.connect(self.verification_code)
        self.pushButton_5.clicked.connect(self.close)
        self.label_5.hide()
        self.label_7.hide()
        self.label_8.hide()
        self.label_9.hide()
        self.label_10.hide()
        self.label_11.hide()
        self.label_12.hide()
        self.label_13.hide()
        self.lineEdit.hide()
        self.pushButton_3.hide()
        self.pushButton_4.hide()
        self.pushButton_5.hide()
        self.messageClient = smsclient.ZhenziSmsClient('https://sms_developer.zhenzikj.com',
'100991','ODFhYzAxNWYtMGYzMS00Yjk5LWE5MmEtY2Y2MDY5YTQyMTFm')

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
    
    def closeEvent(self,event):
        self.isalive = False

    def request(self):
        try:
            if self.usernameLe.text():
                username = self.usernameLe.text()
                print(self.client.sockfd)
                result = self.client.request(self.client.sockfd, username)
                if result:
                    self.usernameLb.setStyleSheet("color:green")
                    self.usernameLb.setText("恭喜您,昵称可用")
                elif result == False:
                    self.usernameLb.setStyleSheet("color:red")
                    self.usernameLb.setText("用户名重复")
            else:
                self.usernameLb.setStyleSheet("color:red")
                self.usernameLb.setText("用户名不能为空")
        except AttributeError:
            pass

    def checkpassword(self):
        if len(self.passwordLe.text()) < 8:
            self.label_4.setText("密码长度太短")
            self.label_4.setStyleSheet("color:red")
        else:
            self.label_4.setText("")
    
    def ensurepassword(self):
        if self.ensureLe.text() != self.passwordLe.text():
            self.label_6.setText("两次输入密码不一致")
            self.label_6.setStyleSheet("color:red")
        else:
            self.label_6.setText("")

    def regest(self):
        if self.usernameLb.text() == "恭喜您,昵称可用" and \
        self.label_4.text() == '' and \
        self.label_6.text() == '' and self.checkBox.isChecked():
            self.hide_and_show()
        else:
            reply = QMessageBox.information(self,"  ","请填写正确的注册信息",QMessageBox.Ok)
            print(reply)

    def hide_and_show(self):
        self.usernameLe.hide()
        self.usernameLb.hide()
        self.radioBtn1.hide()
        self.radioBtn2.hide()
        self.dateEdit.hide()
        self.passwordLe.hide()
        self.label_4.hide()
        self.ensureLe.hide()
        self.label_6.hide()
        self.phonenumberLe.hide()
        self.checkBox.hide()
        self.RegisterBtn.hide()
        self.label_5.show()
        self.label_7.show()
        self.label_8.show()
        self.label_9.show()
        self.lineEdit.show()
        self.pushButton_3.show()
        self.pushButton_4.show()
        self.label_7.setText(self.phonenumberLe.text())
        self.send_message()

    def send_message(self):
        self.code = sendMessage('regist',self.phonenumberLe.text())

    def verification_code(self):
        if self.lineEdit.text() == self.code:
            username = self.usernameLe.text()
            password = self.passwordLe.text()
            if self.radioBtn1.isChecked():
                gender = "0"
            elif self.radioBtn2.isChecked():
                gender = "1"
            birthday = self.dateEdit.text()
            tel = self.phonenumberLe.text()
            (config,count) = self.client.register(username,password,gender,birthday,tel)
            if config == True:
                self.label_5.hide()
                self.label_7.hide()
                self.label_8.hide()
                self.label_9.hide()
                self.lineEdit.hide()
                self.pushButton_3.hide()
                self.pushButton_4.hide()
                self.label_10.show()
                self.label_11.show()
                self.label_12.show()
                self.label_13.show()
                self.pushButton_5.show()
                self.label_12.setText(count)
            elif config == False:
                reply = QMessageBox.information(self,"  ","注册失败",QMessageBox.Ok)
                print(reply)
        else:
            reply = QMessageBox.information(self,"  ","验证码错误",QMessageBox.Ok)
