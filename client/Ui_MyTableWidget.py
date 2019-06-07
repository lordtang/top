from PyQt5.QtWidgets import QTableWidget,QLabel
from PyQt5.QtCore import pyqtSignal

class MyTbaleWidget(QTableWidget):
    # mouse_move = pyqtSignal()
    def __init__(self,parent=None):
        super().__init__(parent)
        self.flag = True

    def enterEvent(self,event):
        self.setMouseTracking(True)

    # def mouseMoveEvent(self,QMouseEvent):
    #     # print(QMouseEvent.globalPos())
    #     # QMouseEvent.accept()
    #     if self.flag:
    #         print(self.parent().pos())
    #         print(QMouseEvent.globalPos())
    #         print(QMouseEvent.x(),QMouseEvent.y())

class MyLabel(QLabel):
    def __init__(self,parent=None):
        super().__init__(parent)
    
    def enterEvent(self,e):
        self.setMouseTracking(True)