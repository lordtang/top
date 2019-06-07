# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\python_work\middle_task\LoginForm.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoginForm(object):
    def setupUi(self, LoginForm):
        LoginForm.setObjectName("LoginForm")
        LoginForm.resize(550, 429)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pic/images/01-4.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LoginForm.setWindowIcon(icon)
        LoginForm.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.LogBtn = QtWidgets.QPushButton(LoginForm)
        self.LogBtn.setGeometry(QtCore.QRect(190, 380, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.LogBtn.setFont(font)
        self.LogBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.LogBtn.setAutoFillBackground(False)
        self.LogBtn.setStyleSheet("border: 0px solid;\n"
"border-radius: 5px;\n"
"background-color: rgb(10, 200, 255);\n"
"color: rgb(255, 255, 255);\n"
"\n"
"")
        self.LogBtn.setObjectName("LogBtn")
        self.RPCheBox = QtWidgets.QCheckBox(LoginForm)
        self.RPCheBox.setGeometry(QtCore.QRect(190, 350, 85, 29))
        self.RPCheBox.setStyleSheet("color: rgb(140, 140, 140);")
        self.RPCheBox.setObjectName("RPCheBox")
        self.RegisterBtn = QtWidgets.QPushButton(LoginForm)
        self.RegisterBtn.setGeometry(QtCore.QRect(420, 280, 61, 28))
        self.RegisterBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.RegisterBtn.setStyleSheet("background-color: transparent;\n"
"color: rgb(140, 140, 140);")
        self.RegisterBtn.setObjectName("RegisterBtn")
        self.ForgetBtn = QtWidgets.QPushButton(LoginForm)
        self.ForgetBtn.setGeometry(QtCore.QRect(420, 320, 61, 28))
        self.ForgetBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ForgetBtn.setStyleSheet("background-color: transparent;\n"
"color: rgb(140, 140, 140);")
        self.ForgetBtn.setObjectName("ForgetBtn")
        self.PicLabel = QtWidgets.QLabel(LoginForm)
        self.PicLabel.setGeometry(QtCore.QRect(80, 280, 91, 91))
        self.PicLabel.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.PicLabel.setText("")
        self.PicLabel.setPixmap(QtGui.QPixmap(":/pic/images/00-5.png"))
        self.PicLabel.setScaledContents(True)
        self.PicLabel.setObjectName("PicLabel")
        self.PwLineEdit = QtWidgets.QLineEdit(LoginForm)
        self.PwLineEdit.setGeometry(QtCore.QRect(190, 320, 211, 30))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.PwLineEdit.setFont(font)
        self.PwLineEdit.setStyleSheet("border-bottom-color: rgb(0, 0, 0);\n"
"border: 0.5px solid gray;")
        self.PwLineEdit.setText("")
        self.PwLineEdit.setFrame(False)
        self.PwLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PwLineEdit.setObjectName("PwLineEdit")
        self.CtComBox = QtWidgets.QComboBox(LoginForm)
        self.CtComBox.setGeometry(QtCore.QRect(190, 280, 211, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        self.CtComBox.setFont(font)
        self.CtComBox.setAutoFillBackground(False)
        self.CtComBox.setStyleSheet("color: rgb(150, 150, 150);\n"
"border-radius: 3px;\n"
"border: 0.5px solid gray;\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 20px;\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 3px;\n"
"    border-bottom-right-radius: 3px;\n"
"}")
        self.CtComBox.setEditable(True)
        self.CtComBox.setCurrentText("")
        self.CtComBox.setDuplicatesEnabled(True)
        self.CtComBox.setFrame(False)
        self.CtComBox.setObjectName("CtComBox")
        self.RPCheBox_2 = QtWidgets.QCheckBox(LoginForm)
        self.RPCheBox_2.setGeometry(QtCore.QRect(320, 350, 85, 29))
        self.RPCheBox_2.setStyleSheet("color: rgb(140, 140, 140);")
        self.RPCheBox_2.setObjectName("RPCheBox_2")
        self.lineEdit = QtWidgets.QLineEdit(LoginForm)
        self.lineEdit.setGeometry(QtCore.QRect(191, 281, 171, 28))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("border: 0px;\n"
"")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayoutWidget = QtWidgets.QWidget(LoginForm)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 551, 261))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        #新建控件
        self.pan = QtWidgets.QLabel(LoginForm)
        self.pan.setGeometry(QtCore.QRect(0,0,520,265))
        self.pan.setStyleSheet("background-color:transparent;color:rgb(255,255,255)")
        self.logo = QtWidgets.QLabel(LoginForm)
        self.logo.setGeometry(QtCore.QRect(0,-15,150,80))
        self.logo.setStyleSheet("background-color:transparent;color:rgb(255,255,255)")
        self.logo.setPixmap(QtGui.QPixmap(":/pic/images/00-4.png"))
        self.logo.setScaledContents(True)
        self.ExitBtn = QtWidgets.QPushButton(LoginForm)
        self.ExitBtn.setGeometry(QtCore.QRect(520, 0, 30, 25))
        self.ExitBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ExitBtn.setAutoFillBackground(False)
        self.ExitBtn.setStyleSheet("background-color:transparent;color:rgb(255,255,255)"
"")
        self.ExitBtn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/pic/images/00-2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ExitBtn.setIcon(icon1)
        self.ExitBtn.setObjectName("ExitBtn")
        self.MinimizeBtn = QtWidgets.QPushButton(LoginForm)
        self.MinimizeBtn.setGeometry(QtCore.QRect(490, 0, 30, 25))
        self.MinimizeBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.MinimizeBtn.setStyleSheet("background-color:transparent")
        self.MinimizeBtn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/pic/images/00-3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.MinimizeBtn.setIcon(icon2)
        self.MinimizeBtn.setDefault(False)
        self.MinimizeBtn.setObjectName("MinimizeBtn")

        self.retranslateUi(LoginForm)
        self.ExitBtn.clicked.connect(LoginForm.close)
        self.MinimizeBtn.clicked.connect(LoginForm.showMinimized)
        QtCore.QMetaObject.connectSlotsByName(LoginForm)
        LoginForm.setTabOrder(self.lineEdit, self.PwLineEdit)
        LoginForm.setTabOrder(self.PwLineEdit, self.LogBtn)
        LoginForm.setTabOrder(self.LogBtn, self.RPCheBox)
        LoginForm.setTabOrder(self.RPCheBox, self.RPCheBox_2)
        LoginForm.setTabOrder(self.RPCheBox_2, self.RegisterBtn)
        LoginForm.setTabOrder(self.RegisterBtn, self.ForgetBtn)
        LoginForm.setTabOrder(self.ForgetBtn, self.CtComBox)

    def retranslateUi(self, LoginForm):
        _translate = QtCore.QCoreApplication.translate
        LoginForm.setWindowTitle(_translate("LoginForm", "欢迎使用Top"))
        self.LogBtn.setText(_translate("LoginForm", "登录"))
        self.RPCheBox.setText(_translate("LoginForm", "记住密码"))
        self.RegisterBtn.setText(_translate("LoginForm", "注册账号"))
        self.ForgetBtn.setText(_translate("LoginForm", "忘记密码"))
        self.PwLineEdit.setPlaceholderText(_translate("LoginForm", "请输入密码"))
        self.RPCheBox_2.setText(_translate("LoginForm", "自动登录"))
        self.lineEdit.setPlaceholderText(_translate("LoginForm", "请输入账号"))

import LoginSource_rc
