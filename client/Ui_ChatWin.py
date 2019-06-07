# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\python_work\middle_task\ChatWin.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets,Qt

class Ui_ChatWin(object):
    def setupUi(self, ChatWin):
        ChatWin.setObjectName("ChatWin")
        ChatWin.resize(1050, 700)
        ChatWin.setMinimumSize(QtCore.QSize(1050, 700))
        self.horizontalLayout = QtWidgets.QHBoxLayout(ChatWin)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(ChatWin)
        self.frame.setMaximumSize(QtCore.QSize(90, 16777215))
        self.frame.setAcceptDrops(False)
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("background-color: rgb(30, 180, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_5 = QtWidgets.QFrame(self.frame)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.pushButton = MyPushButton(self.frame_5)
        self.pushButton.setGeometry(QtCore.QRect(8, 85, 51, 51))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("background-color: transparent;")
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pic/images/03-2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(45, 45))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = MyPushButton2(self.frame_5)
        self.pushButton_2.setGeometry(QtCore.QRect(8, 135, 51, 51))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet("background-color: transparent;")
        self.pushButton_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/pic/images/03-3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setIconSize(QtCore.QSize(38, 38))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = MyPushButton3(self.frame_5)
        self.pushButton_3.setGeometry(QtCore.QRect(8, 185, 51, 51))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setStyleSheet("background-color:transparent;")
        self.pushButton_3.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/pic/images/03-4.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = MyPushButton4(self.frame_5)
        self.pushButton_4.setGeometry(QtCore.QRect(8, 235, 50, 50))
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setStyleSheet("background-color: transparent;")
        self.pushButton_4.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/pic/images/03-5.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon3)
        self.pushButton_4.setIconSize(QtCore.QSize(43, 43))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_10 = QtWidgets.QPushButton(self.frame_5)
        self.pushButton_10.setGeometry(QtCore.QRect(3, 3, 60, 60))
        self.pushButton_10.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border:0px;")
        self.pushButton_10.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/pic/images/03-1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_10.setIcon(icon4)
        self.pushButton_10.setIconSize(QtCore.QSize(55, 55))
        self.pushButton_10.setObjectName("pushButton_10")
        self.label_3 = QtWidgets.QLabel(self.frame_5)
        self.label_3.setGeometry(QtCore.QRect(35, 83, 20, 20))
        self.label_3.setStyleSheet("border-radius: 10px;\n"
"border:0.5px solid grey;\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(255, 0, 0);")
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.frame_5)
        self.frame_6 = QtWidgets.QFrame(self.frame)
        self.frame_6.setMinimumSize(QtCore.QSize(66, 0))
        self.frame_6.setMaximumSize(QtCore.QSize(66, 200))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.pushButton_7 = MyPushButton7(self.frame_6)
        self.pushButton_7.setGeometry(QtCore.QRect(10, 140, 51, 51))
        self.pushButton_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_7.setStyleSheet("background-color: transparent;")
        self.pushButton_7.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/pic/images/03-8.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon5)
        self.pushButton_7.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_6 = MyPushButton6(self.frame_6)
        self.pushButton_6.setGeometry(QtCore.QRect(10, 80, 51, 50))
        self.pushButton_6.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_6.setStyleSheet("background-color: transparent;")
        self.pushButton_6.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/pic/images/03-7.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon6)
        self.pushButton_6.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_5 = MyPushButton5(self.frame_6)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 20, 51, 50))
        self.pushButton_5.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_5.setStyleSheet("background-color: transparent;")
        self.pushButton_5.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/pic/images/03-6.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon7)
        self.pushButton_5.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout.addWidget(self.frame_6)
        self.horizontalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(ChatWin)
        self.frame_2.setMinimumSize(QtCore.QSize(240, 0))
        self.frame_2.setStyleSheet("background-color: rgb(245, 245, 245);\n"
"\n"
"")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_7 = QtWidgets.QFrame(self.frame_2)
        self.frame_7.setMinimumSize(QtCore.QSize(0, 80))
        self.frame_7.setMaximumSize(QtCore.QSize(16777215, 80))
        self.frame_7.setStyleSheet("border:0px;")
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.frame_7)
        self.pushButton_8.setGeometry(QtCore.QRect(190, 30, 30, 30))
        self.pushButton_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_8.setStyleSheet("border: 0.5px solid grey;\n"
"border-radius: 10px;\n"
"background-color: rgb(240, 240, 240);")
        self.pushButton_8.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/pic/images/03-14.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_8.setIcon(icon8)
        self.pushButton_8.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_8.setObjectName("pushButton_8")
        self.frame_9 = QtWidgets.QFrame(self.frame_7)
        self.frame_9.setGeometry(QtCore.QRect(20, 30, 161, 30))
        self.frame_9.setStyleSheet("border: 0.5px solid grey;\n"
"border-radius: 10px;\n"
"background-color: rgb(240, 240, 240);")
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.lineEdit = QtWidgets.QLineEdit(self.frame_9)
        self.lineEdit.setGeometry(QtCore.QRect(30, 1, 130, 28))
        self.lineEdit.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.lineEdit.setStyleSheet("border:0px;")
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.frame_9)
        self.label.setGeometry(QtCore.QRect(1, 1, 28, 28))
        self.label.setStyleSheet("border:0px;")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/pic/images/03-19.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.frame_7)
        self.frame_8 = QtWidgets.QFrame(self.frame_2)
        self.frame_8.setStyleSheet("border:0px;\n"
"")
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.tableWidget_2 = MyTableWidget(self.frame_8)
        self.tableWidget_2.setGeometry(QtCore.QRect(0, 0, 241, 621))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.verticalLayout_3.addWidget(self.frame_8)
        self.horizontalLayout.addWidget(self.frame_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_3 = QtWidgets.QFrame(ChatWin)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 80))
        self.frame_3.setStyleSheet("background-color: rgb(250, 250, 250);\n"
"border-bottom:0.5px solid rgb(240,240,240);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 90, 36))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_2.setStyleSheet("border: 0px;\n"
"")
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setObjectName("label_2")
        self.pushButton_12 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_12.setGeometry(QtCore.QRect(655, 0, 30, 30))
        self.pushButton_12.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_12.setStyleSheet("border:0px")
        self.pushButton_12.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/pic/images/03-10.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_12.setIcon(icon9)
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_13 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_13.setGeometry(QtCore.QRect(625, 0, 30, 30))
        self.pushButton_13.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_13.setStyleSheet("border:0px;")
        self.pushButton_13.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/pic/images/03-9.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_13.setIcon(icon10)
        self.pushButton_13.setObjectName("pushButton_13")
        self.pushButton_11 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_11.setGeometry(QtCore.QRect(685, 0, 31, 30))
        self.pushButton_11.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_11.setStyleSheet("border:0px;")
        self.pushButton_11.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/pic/images/03-11.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_11.setIcon(icon11)
        self.pushButton_11.setObjectName("pushButton_11")
        self.verticalLayout_2.addWidget(self.frame_3)
        self.tableWidget = MyTableWidget(ChatWin)
        self.tableWidget.setStyleSheet("border:0px;\n"
"background-color: rgb(250, 250, 250);")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.frame_4 = QtWidgets.QFrame(ChatWin)
        self.frame_4.setMinimumSize(QtCore.QSize(0, 200))
        self.frame_4.setStyleSheet("background-color: rgb(250, 250, 250);\n"
"border-top:0.5px solid rgb(240,240,240);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.pushButton_9 = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_9.setGeometry(QtCore.QRect(660, 10, 51, 41))
        self.pushButton_9.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_9.setStyleSheet("background-color: transparent;border:0px;")
        self.pushButton_9.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/pic/images/03-13.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_9.setIcon(icon12)
        self.pushButton_9.setIconSize(QtCore.QSize(40, 30))
        self.pushButton_9.setObjectName("pushButton_9")
        self.textEdit = QtWidgets.QTextEdit(self.frame_4)
        self.textEdit.setGeometry(QtCore.QRect(20, 56, 681, 91))
        self.textEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.textEdit.setStyleSheet("border:0px;")
        self.textEdit.verticalScrollBar().setStyleSheet('''
        QScrollBar:vertical{
            background:rgb(245,245,245);
            padding-top:0px;
            padding-bottom:0px;
            padding-left:0px;
            padding-right:0px;
            border-left:0px solid #d7d7d7;
            width:10px;}
        QScrollBar::handle:vertical{
            background:#dbdbdb;
            border-radius:5px;
            min-height:80px;}
        QScrollBar::handle:vertical:hover{
            background:#d0d0d0;}
        ''')
        self.textEdit.setObjectName("textEdit")
        self.pushButton_14 = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_14.setGeometry(QtCore.QRect(610, 10, 51, 41))
        self.pushButton_14.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_14.setStyleSheet("background-color: transparent;border:0px;")
        self.pushButton_14.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/pic/images/03-12.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_14.setIcon(icon13)
        self.pushButton_14.setIconSize(QtCore.QSize(40, 30))
        self.pushButton_14.setObjectName("pushButton_14")
        self.pushButton_15 = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_15.setGeometry(QtCore.QRect(610, 150, 91, 41))
        self.pushButton_15.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_15.setStyleSheet("border: 0px solid grey;\n"
"border-radius: 10px;\n"
"background-color: rgb(229, 229, 229);\n"
"")
        self.pushButton_15.setObjectName("pushButton_15")
        self.pushButton_16 = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_16.setGeometry(QtCore.QRect(15, 10, 40, 40))
        self.pushButton_16.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_16.setStyleSheet("background-color: transparent;\n"
"border:0px;")
        self.pushButton_16.setText("")
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/pic/images/03-15.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_16.setIcon(icon14)
        self.pushButton_16.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_16.setObjectName("pushButton_16")
        self.pushButton_17 = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_17.setGeometry(QtCore.QRect(60, 10, 40, 40))
        self.pushButton_17.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_17.setStyleSheet("background-color: transparent;border:0px;")
        self.pushButton_17.setText("")
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/pic/images/03-16.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_17.setIcon(icon15)
        self.pushButton_17.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_17.setObjectName("pushButton_17")
        self.pushButton_18 = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_18.setGeometry(QtCore.QRect(105, 10, 40, 40))
        self.pushButton_18.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_18.setStyleSheet("background-color: transparent;border:0px;")
        self.pushButton_18.setText("")
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/pic/images/03-17.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_18.setIcon(icon16)
        self.pushButton_18.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_18.setObjectName("pushButton_18")
        self.pushButton_19 = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_19.setGeometry(QtCore.QRect(150, 10, 40, 40))
        self.pushButton_19.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_19.setStyleSheet("background-color: transparent;border:0px;")
        self.pushButton_19.setText("")
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/pic/images/03-18.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_19.setIcon(icon17)
        self.pushButton_19.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_19.setObjectName("pushButton_19")
        self.verticalLayout_2.addWidget(self.frame_4)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(ChatWin)
        self.pushButton_11.clicked.connect(ChatWin.close)
        self.pushButton_12.clicked.connect(ChatWin.showMaximized)
        self.pushButton_13.clicked.connect(ChatWin.showMinimized)
        QtCore.QMetaObject.connectSlotsByName(ChatWin)

    def retranslateUi(self, ChatWin):
        _translate = QtCore.QCoreApplication.translate
        ChatWin.setWindowTitle(_translate("ChatWin", "ChatWin"))
        self.label_3.setText(_translate("ChatWin", "9"))
        self.lineEdit.setPlaceholderText(_translate("ChatWin", "搜索"))
        self.label_2.setText(_translate("ChatWin", "小仙女"))
        self.pushButton_15.setText(_translate("ChatWin", "发送"))
        self.textEdit.setShortcutEnabled(True)


class MyTableWidget(QtWidgets.QTableWidget):
        def __init__(self,parent=None):
                super().__init__(parent)

        def enterEvent(self,e):
                self.verticalScrollBar().setVisible(True)
        
        def leaveEvent(self,e):
                self.verticalScrollBar().setVisible(False)

# class MyTextEdit(QtWidgets.QTextEdit):
#         _EnterPress = QtCore.pyqtSignal()
#         def __init__(self,parent=None):
#                 super().__init__(parent)

#         def keyPressEvent(self,e):
#                 if e.key()==Qt.Qt.Key_Return:
#                         self._EnterPress.emit()
#                 else:
#                         self.setText("<img src='varifyCode.png'>")

class MyPushButton(QtWidgets.QPushButton):
        def __init__(self,parent=None):
                super().__init__(parent)

        def enterEvent(self,e):
                self.setIconSize(QtCore.QSize(46,46))
        def leaveEvent(self,e):
                self.setIconSize(QtCore.QSize(45,45))

class MyPushButton2(QtWidgets.QPushButton):
        def __init__(self,parent=None):
                super().__init__(parent)

        def enterEvent(self,e):
                self.setIconSize(QtCore.QSize(40,40))
        def leaveEvent(self,e):
                self.setIconSize(QtCore.QSize(38,38))

class MyPushButton3(QtWidgets.QPushButton):
        def __init__(self,parent=None):
                super().__init__(parent)

        def enterEvent(self,e):
                self.setIconSize(QtCore.QSize(37,37))
        def leaveEvent(self,e):
                self.setIconSize(QtCore.QSize(35,35))

class MyPushButton4(QtWidgets.QPushButton):
        def __init__(self,parent=None):
                super().__init__(parent)

        def enterEvent(self,e):
                self.setIconSize(QtCore.QSize(45,45))
        def leaveEvent(self,e):
                self.setIconSize(QtCore.QSize(43,43))

class MyPushButton5(QtWidgets.QPushButton):
        def __init__(self,parent=None):
                super().__init__(parent)

        def enterEvent(self,e):
                self.setIconSize(QtCore.QSize(42,42))
        def leaveEvent(self,e):
                self.setIconSize(QtCore.QSize(40,40))

class MyPushButton6(QtWidgets.QPushButton):
        def __init__(self,parent=None):
                super().__init__(parent)

        def enterEvent(self,e):
                self.setIconSize(QtCore.QSize(42,42))
        def leaveEvent(self,e):
                self.setIconSize(QtCore.QSize(40,40))

class MyPushButton7(QtWidgets.QPushButton):
        def __init__(self,parent=None):
                super().__init__(parent)

        def enterEvent(self,e):
                self.setIconSize(QtCore.QSize(42,42))
        def leaveEvent(self,e):
                self.setIconSize(QtCore.QSize(40,40))

import ChatFormSource_rc
