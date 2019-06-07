from PyQt5 import QtGui, Qt, QtCore
from PyQt5.QtWidgets import QPushButton,QApplication,QWidget

def getIcon(path):
    # filename = ''.join(path.split('/')[-1].split('.')[:-1])
    icon, name = getFileInfo(path)
    icon_path = 'temp_info\\file_icon\\%s.png'%name
    icon.pixmap(48,48).save(icon_path)
    return icon_path,name
    

def getFileInfo(path):
    """获取文件的图片和名字"""
    fileInfo = Qt.QFileInfo(path)
    fileIcon = Qt.QFileIconProvider()
    icon = QtGui.QIcon(fileIcon.icon(fileInfo))
    name = QtCore.QFileInfo(path).fileName()
    return icon,name
