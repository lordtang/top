from PyQt5.QtWidgets import QWidget,QApplication,QPushButton,QFrame,QLabel,QLineEdit
from PyQt5 import QtGui,QtCore
import os

class FriendFrame(QFrame):
    def __init__(self,myID,info_list,parent=None):
        super().__init__(parent)
        self.parent = parent
        self.info_list = info_list
        self.myID = myID
        self.setItem()
        self.resize(718,668)
        self.setStyleSheet("background-color:rgb(250,250,250);")
        self.button.clicked.connect(self.frame_button_click)

    def setItem(self):
        #发消息按钮
        self.button = QPushButton(self)
        self.button.setText("发消息")
        self.button.setStyleSheet('''background-color:rgb(30,180,255);color:rgb(255,255,255);border: 0px solid;
        border-radius: 10px;''')
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.button.setFont(font)
        self.button.setGeometry(260,500,180,50)
        #好友昵称Label
        self.name_label = QLabel(self)
        self.name_label.setText(self.info_list[1])
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(18)
        font.setWeight(75)
        self.name_label.setFont(font)
        self.name_label.setGeometry(100,60,250,60)
        #好友性别Label
        pwd = os.getcwd()
        path = pwd + '\\images\\03-20.png'
        self.gender_label = QLabel(self)
        self.gender_label.setGeometry(330,80,30,30)
        self.gender_label.setPixmap(QtGui.QPixmap(path))
        self.gender_label.setScaledContents(True)
        #好友签名Label
        self.sign_label = QLabel(self)
        self.sign_label.setGeometry(100,130,400,30)
        self.sign_label.setText("这个家伙很懒，没有设置签名")
        self.sign_label.setStyleSheet("color:grey;")
        #好友头像Label
        self.head_label = QLabel(self)
        self.head_label.setGeometry(510,70,90,90)
        self.head_label.setPixmap(QtGui.QPixmap(self.info_list[2]))
        self.head_label.setScaledContents(True)

        #分割线
        self.devision_line = QLabel(self)
        self.devision_line.setGeometry(100,200,500,2)
        self.devision_line.setStyleSheet("border:0.5px solid rgb(240,240,240);")
        #备注label
        self.remark = QLabel(self)
        self.remark.setGeometry(100,240,100,40)
        self.remark.setText("备 注")
        self.remark.setStyleSheet("color:grey;")
        #修改备注Button
        self.remark_btn = QPushButton(self)
        self.remark_btn.setText("点击添加备注")
        self.remark_btn.setGeometry(160,240,200,40)
        self.remark_btn.setStyleSheet("background-color:transparent;border:0px;")

        #修改备注LineEdit
        self.remark_lineEdit = QLineEdit(self)
        self.remark_lineEdit.setGeometry(215,240,200,30)
        self.remark_lineEdit.hide()
        #生日Label
        self.birth = QLabel(self)
        self.birth.setGeometry(100,300,100,40)
        self.birth.setText("生 日")
        self.birth.setStyleSheet("color:grey;")
        #出生日期
        self.birthday = QLabel(self)
        self.birthday.setGeometry(215,300,100,40)
        self.birthday.setText("1999-10-01")
        #星座
        self.constellation = QLabel(self)
        self.constellation.setGeometry(350,300,100,40)
        self.constellation.setText("天秤座")
        #Top账号
        self.top_count = QLabel(self)
        self.top_count.setGeometry(100,360,100,40)
        self.top_count.setText("Top账号")
        self.top_count.setStyleSheet("color:grey;")
        #账号
        self.count = QLabel(self)
        self.count.setGeometry(215,360,100,40)
        self.count.setText(self.info_list[0])
        #分割线
        self.devision_line1 = QLabel(self)
        self.devision_line1.setGeometry(100,450,500,2)
        self.devision_line1.setStyleSheet("border:0.5px solid rgb(240,240,240);")

    def frame_button_click(self):#响应好友信息窗口的发送消息按钮
        self.close()
        with open('Top files\\%s\\temp_conversation.txt'%self.myID,'rt') as f:
            temp_conver_list = f.readlines()
        with open('Top files\\%s\\temp_conversation.txt'%self.myID,'at') as f:
            if self.info_list[0]+'\n' not in temp_conver_list:
                f.write(self.info_list[0]+'\n')
        self.parent.invert_message_status(self.parent.name_count[1])
        self.parent.create_friend_list()
        self.parent.tableWidget_2.hide()
        self.parent.new_table.show()
        self.parent.create_message_item(self.parent.name_count[1])