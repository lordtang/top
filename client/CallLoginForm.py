import sys,os
from PyQt5.QtWidgets import QApplication,QWidget,QMessageBox,QComboBox,QPushButton
from PyQt5.QtCore import Qt,pyqtSignal,QUrl
from PyQt5 import QtGui,QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView
from threading import Thread
from struct import Struct

from Ui_LoginForm import Ui_LoginForm
from CallChatWin import ChatWin
from CallRegister import Register
from CallFogetDialog import Forget
from client_copy import PrivateChatRoomClient

class LoginWin(QWidget,Ui_LoginForm):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)#设置无边框
        self.CtComBox.currentIndexChanged.connect(self.changeLineText)
        self.LogBtn.clicked.connect(self.login) #登录
        self.RegisterBtn.clicked.connect(self.registershow)
        self.ForgetBtn.clicked.connect(self.forgetshow)
        self.client = PrivateChatRoomClient()
        self.client.open_client()
        icon_path = os.getcwd()
        icon_path = icon_path.replace('\\','/')
        self.CtComBox.setStyleSheet("""
        QComboBox{border-radius: 3px;border: 0.5px solid gray;}
        QComboBox::down-arrow{image:url("%s/images/00-1.png");}
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 26px;
            border-left-width: 0.5px;
            border-left-color: darkgray;
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;}
        """%icon_path)
        self.load_login_record()
        self.lineEdit.setText(self.CtComBox.currentText())
        self.webView = QWebEngineView()
        index_path = os.getcwd() + '\\jiaoben6471\\index.html'
        index_path = index_path.replace('\\','/')
        self.webView.load(QUrl(index_path))
        self.gridLayout.addWidget(self.webView)
        self.gridLayout.setEnabled(False)
        
    def changeLineText(self):
        self.lineEdit.setText(self.CtComBox.currentText())
        for i in self.login_record:
            if i == self.CtComBox.currentText():
                self.PwLineEdit.setText(self.login_record[i])
                break

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
    
    def login(self):
        count = self.lineEdit.text()
        password = self.PwLineEdit.text()
        result = self.client.do_login(self.client.sockfd, count, password)
        print("登录请求结果:",result)
        if result:
            while True:
                try:    
                    data,friends_info = self.client.log_success_recv(self.client.sockfd)
                except Exception:
                    continue
                else:
                    break
            u_count = data[0].decode()
            u_name = data[1].decode()
            u_tel = data[2].decode()
            u_birth = data[3].decode()
            u_gender = data[4].decode()
            self.new_files(u_count) #新建缓存文件
            try:
                with open('temp_info/u_head_portrait.jpg','wb') as f:
                    f.write(data[5])
                f.close()
            except FileNotFoundError:
                pass
            u_head_portrait = 'temp_info/u_head_portrait.jpg'
            my_info_list = [u_count, u_name, u_tel, u_birth, u_gender, u_head_portrait]
            friends_info_list = {}
            for i in friends_info:
                key = i.decode()
                value = []
                value.append(friends_info[i][0].decode())
                try:
                    path = 'temp_info/%s.jpg'%i.decode()
                    with open(path, 'wb') as f:
                        f.write(friends_info[i][1])
                    f.close()
                except FileNotFoundError:
                    pass
                value.append(path)
                friends_info_list[key]=value
            self.chatwin = ChatWin(self.client,my_info=my_info_list,friends_info=friends_info_list)
            self.chatwin.show()
            self.close()
    
    def new_files(self,u_count):
        pwd = os.getcwd()
        dir1 = pwd + '\\Top files\\' + u_count
        dir2 = pwd + '\\Top files\\' + u_count + '\\FileRecv'
        dir3 = pwd + '\\Top files\\' + u_count + '\\image\\C2C'
        dir4 = pwd + '\\Top files\\' + u_count + '\\image\\Group'
        if not os.path.exists(dir1):
            os.makedirs(dir1)
        if not os.path.exists(dir2):
            os.makedirs(dir2)
        if not os.path.exists(dir3):
            os.makedirs(dir3)
        if not os.path.exists(dir4):
            os.makedirs(dir4)
        path1 = pwd + '\\Top files\\' + u_count + '\\temp_message.txt'
        path2 = pwd + '\\Top files\\' + u_count + '\\message_record.txt'
        path3 = pwd + '\\Top files\\' + u_count + '\\temp_conversation.txt'
        if not os.path.exists(path1):
            f = open(path1,'x')
            f.close()
        if not os.path.exists(path2):
            f = open(path2,'x')
            f.close()
        if not os.path.exists(path3):
            f = open(path3,'x')
            f.close()
    
    def registershow(self):
        self.registerwin = Register(self.client)
        self.registerwin.show()
        def cyclic_display():
            import time
            img_path = os.getcwd() + '\\images\\'
            img_path = img_path.replace('\\','/')
            while True:
                self.registerwin.label.setPixmap(QtGui.QPixmap(img_path + "01-1.jpg"))
                time.sleep(4)
                self.registerwin.label.setPixmap(QtGui.QPixmap(img_path + "01-2.jpg"))
                time.sleep(4)
                self.registerwin.label.setPixmap(QtGui.QPixmap(img_path + "01-3.jpg"))
                time.sleep(4)
                print(self.registerwin.isalive)
                if self.registerwin.isalive == False:
                    break
        thread = Thread(target=cyclic_display)
        thread.setDaemon(True)
        thread.start()

    def forgetshow(self):
        self.forgetwin = Forget(self.client)
        self.forgetwin.show()

    def load_login_record(self):
        self.login_record = {}
        try:
            path = os.getcwd()
            path = path.replace('\\','/') + '/login_record.txt'
            f = open(path, 'r')
        except Exception:
            pass
        else:
            for i in f.readlines():
                data = i.split(' ')
                self.login_record[data[0]] = data[1].rstrip()
                self.CtComBox.addItem(data[0])
                if not self.PwLineEdit.text():
                    self.PwLineEdit.setText(data[1].rstrip())
            f.close()

def CallLoginForm():
    app = QApplication(sys.argv)
    win = LoginWin()
    win.show()
    sys.exit(app.exec_())