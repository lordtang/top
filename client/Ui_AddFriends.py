# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\python_work\middle_task\AddFriends.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddFriends(object):
    def setupUi(self, AddFriends):
        AddFriends.setObjectName("AddFriends")
        AddFriends.resize(700, 420)
        AddFriends.setStyleSheet("background-color: #EBF2F9;")
        self.label = QtWidgets.QLabel(AddFriends)
        self.label.setGeometry(QtCore.QRect(0, 0, 711, 81))
        self.label.setStyleSheet("background-color: rgb(0, 155, 219);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(AddFriends)
        self.pushButton.setGeometry(QtCore.QRect(310, 40, 93, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: transparent;")
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(AddFriends)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 41, 41))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.Close = QtWidgets.QPushButton(AddFriends)
        self.Close.setGeometry(QtCore.QRect(665, 0, 35, 28))
        self.Close.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Close.setStyleSheet("border:0px;\n"
"background-color: transparent;")
        self.Close.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/07-04.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Close.setIcon(icon)
        self.Close.setIconSize(QtCore.QSize(20, 20))
        self.Close.setObjectName("Close")
        self.Mini = QtWidgets.QPushButton(AddFriends)
        self.Mini.setGeometry(QtCore.QRect(630, 0, 35, 28))
        self.Mini.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Mini.setStyleSheet("border:0px;\n"
"background-color: transparent;")
        self.Mini.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/07-03.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Mini.setIcon(icon1)
        self.Mini.setIconSize(QtCore.QSize(20, 20))
        self.Mini.setObjectName("Mini")
        self.lineEdit = QtWidgets.QLineEdit(AddFriends)
        self.lineEdit.setGeometry(QtCore.QRect(130, 90, 341, 31))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius:5px;\n"
"border:0.5px solid rgb(0, 155, 219);")
        self.lineEdit.setInputMask("")
        self.lineEdit.setObjectName("lineEdit")
        self.Find = QtWidgets.QPushButton(AddFriends)
        self.Find.setGeometry(QtCore.QRect(480, 100, 161, 51))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.Find.setFont(font)
        self.Find.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Find.setStyleSheet("background-color: rgb(0, 155, 219);\n"
"border-radius:5px;\n"
"color: rgb(255, 255, 255);")
        self.Find.setObjectName("Find")
        self.label_4 = QtWidgets.QLabel(AddFriends)
        self.label_4.setGeometry(QtCore.QRect(50, 0, 31, 31))
        self.label_4.setStyleSheet("background-color:transparent;\n"
"color: rgb(255, 255, 255);")
        self.label_4.setObjectName("label_4")
        self.line = QtWidgets.QFrame(AddFriends)
        self.line.setGeometry(QtCore.QRect(0, 170, 700, 3))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_3 = QtWidgets.QLabel(AddFriends)
        self.label_3.setGeometry(QtCore.QRect(10, 180, 72, 15))
        font = QtGui.QFont()
        font.setFamily("新宋体")
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(110, 110, 110);")
        self.label_3.setObjectName("label_3")
        self.frame = QtWidgets.QFrame(AddFriends)
        self.frame.setGeometry(QtCore.QRect(130, 130, 160, 31))
        self.frame.setStyleSheet("border:0.5px solid grey;\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:5px;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect(30, 1, 129, 29))
        self.comboBox.setStyleSheet("QComboBox{border-radius: 3px;\n"
"border:0px;\n"
"background-color:rgb(255,255,255)}\n"
"QComboBox::down-arrow{image:url(\"images/00-1.png\");}\n"
"QComboBox::drop-down {\n"
"            subcontrol-origin: padding;\n"
"            subcontrol-position: top right;\n"
"            width: 26px;\n"
"            border-left-width: 0.5px;\n"
"            border-left-color: darkgray;\n"
"            border-left-style: solid;\n"
"            border-top-right-radius: 3px;\n"
"            border-bottom-right-radius: 3px;}\n"
"        ")
        self.comboBox.setEditable(False)
        self.comboBox.setCurrentText("")
        self.comboBox.setObjectName("comboBox")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(1, 1, 29, 29))
        self.label_5.setStyleSheet("border:0px;")
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("images/07-01.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.frame_2 = QtWidgets.QFrame(AddFriends)
        self.frame_2.setGeometry(QtCore.QRect(310, 130, 160, 31))
        self.frame_2.setStyleSheet("border:0.5px solid grey;\n"
"background-color: rgb(255, 255, 255);\n"
"border-radius:5px;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.comboBox_2 = QtWidgets.QComboBox(self.frame_2)
        self.comboBox_2.setGeometry(QtCore.QRect(30, 1, 129, 29))
        self.comboBox_2.setStyleSheet("QComboBox{border-radius: 3px;\n"
"border:0px;\n"
"background-color:rgb(255,255,255)}\n"
"QComboBox::down-arrow{image:url(\"images/00-1.png\");}\n"
"QComboBox::drop-down {\n"
"            subcontrol-origin: padding;\n"
"            subcontrol-position: top right;\n"
"            width: 26px;\n"
"            border-left-width: 0.5px;\n"
"            border-left-color: darkgray;\n"
"            border-left-style: solid;\n"
"            border-top-right-radius: 3px;\n"
"            border-bottom-right-radius: 3px;}\n"
"        ")
        self.comboBox_2.setEditable(False)
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(1, 1, 29, 29))
        self.label_6.setStyleSheet("border:0px;")
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("images/07-05.png"))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(AddFriends)
        self.label_7.setGeometry(QtCore.QRect(310, 180, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.scrollArea = QtWidgets.QScrollArea(AddFriends)
        self.scrollArea.setGeometry(QtCore.QRect(0, 205, 700, 215))
        self.scrollArea.setStyleSheet("border:0px;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 700, 215))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(AddFriends)
        self.comboBox.setCurrentIndex(-1)
        self.comboBox_2.setCurrentIndex(-1)
        self.Close.clicked.connect(AddFriends.close)
        self.Mini.clicked.connect(AddFriends.showMinimized)
        QtCore.QMetaObject.connectSlotsByName(AddFriends)

    def retranslateUi(self, AddFriends):
        _translate = QtCore.QCoreApplication.translate
        AddFriends.setWindowTitle(_translate("AddFriends", "AddFriends"))
        self.pushButton.setText(_translate("AddFriends", "添加好友"))
        self.label_2.setStyleSheet(_translate("AddFriends", "border:0px;\n"
"background-color: transparent;"))
        self.lineEdit.setPlaceholderText(_translate("AddFriends", "请输入账号/昵称"))
        self.Find.setText(_translate("AddFriends", "查找"))
        self.label_4.setText(_translate("AddFriends", "查找"))
        self.label_3.setText(_translate("AddFriends", "查找结果"))
        self.label_7.setText(_translate("AddFriends", "查找失败"))

