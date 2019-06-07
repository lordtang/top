# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'f:\python_work\middle_task\FileSR.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FileSendRecv(object):
    def setupUi(self, FileSendRecv):
        FileSendRecv.setObjectName("FileSendRecv")
        FileSendRecv.resize(350, 700)
        FileSendRecv.setMinimumSize(QtCore.QSize(100, 700))
        FileSendRecv.setStyleSheet("background-color: rgb(245, 245, 245);")
        self.IconLabel = QtWidgets.QLabel(FileSendRecv)
        self.IconLabel.setGeometry(QtCore.QRect(10, 10, 60, 70))
        self.IconLabel.setStyleSheet("border:0.5px solid grey;\n"
"")
        self.IconLabel.setText("")
        self.IconLabel.setObjectName("IconLabel")
        self.FilenameLabel = QtWidgets.QLabel(FileSendRecv)
        self.FilenameLabel.setGeometry(QtCore.QRect(80, 10, 261, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.FilenameLabel.setFont(font)
        self.FilenameLabel.setObjectName("FilenameLabel")
        self.progressBar = QtWidgets.QProgressBar(FileSendRecv)
        self.progressBar.setGeometry(QtCore.QRect(80, 35, 261, 15))
        self.progressBar.setStyleSheet("padding-right:0px;\n"
"border-radius:3px;\n"
"background-color: rgb(222, 222, 222);")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        self.StatusLabel = QtWidgets.QLabel(FileSendRecv)
        self.StatusLabel.setGeometry(QtCore.QRect(80, 63, 100, 16))
        self.StatusLabel.setStyleSheet("color: rgb(136, 136, 136);")
        self.StatusLabel.setObjectName("StatusLabel")
        self.CancelButton = QtWidgets.QPushButton(FileSendRecv)
        self.CancelButton.setGeometry(QtCore.QRect(303, 63, 41, 16))
        self.CancelButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.CancelButton.setStyleSheet("border:0px;\n"
"color: #12B7F5;")
        self.CancelButton.setObjectName("CancelButton")
        self.RecvButton = QtWidgets.QPushButton(FileSendRecv)
        self.RecvButton.setGeometry(QtCore.QRect(260, 63, 41, 16))
        self.RecvButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.RecvButton.setStyleSheet("border:0px;\n"
"color: #12B7F5;")
        self.RecvButton.setObjectName("RecvButton")

        self.retranslateUi(FileSendRecv)
        QtCore.QMetaObject.connectSlotsByName(FileSendRecv)

    def retranslateUi(self, FileSendRecv):
        _translate = QtCore.QCoreApplication.translate
        FileSendRecv.setWindowTitle(_translate("FileSendRecv", "FileSendRecv"))
        self.FilenameLabel.setText(_translate("FileSendRecv", "文件名(大小MB)"))
        self.StatusLabel.setText(_translate("FileSendRecv", "传输连接中"))
        self.CancelButton.setText(_translate("FileSendRecv", "取消"))
        self.RecvButton.setText(_translate("FileSendRecv", "接收"))

