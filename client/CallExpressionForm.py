from PyQt5.QtWidgets import QApplication,QTableWidgetItem,QFrame,QTableWidget
from PyQt5 import QtGui,QtCore,Qt
import sys

from settings import expression_dic


class ExpressionForm(QFrame):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.tableWidget = QTableWidget(self)
        self.setStyleSheet("background-color:transparent;")
        self.resize(1050,700)
        self.move(0,0)
        self.tableWidget.resize(500,260)
        self.tableWidget.move(280,200)
        self.frame = QFrame(self)
        self.frame.resize(500,50)
        self.frame.move(280,460)
        self.frame.setStyleSheet("background-color:white")
        self.make_icon()

    def make_icon(self):
        self.tableWidget.setShowGrid(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setStyleSheet('''
        QTableWidget {border:10px solid white;background-color:white}
        QTableWidget:item:hover {background-color:rgb(230,230,230);}''')
        self.tableWidget.setRowCount(6)
        self.tableWidget.setColumnCount(12)
        self.tableWidget.setIconSize(QtCore.QSize(40,40))
        for i in range(6):
            self.tableWidget.setRowHeight(i,40)
            for j in range(12):
                self.tableWidget.setColumnWidth(j,40)
                head_pic = QTableWidgetItem()
                head_pic.setToolTip(expression_dic["10%d%d.png"%(i,j)])
                icon = QtGui.QIcon("expression/fun/10%d%d.png"%(i,j))
                head_pic.setIcon(QtGui.QIcon(icon))
                self.tableWidget.setItem(i,j,head_pic)

