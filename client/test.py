# from PIL import Image
# from PyQt5.QtWidgets import QTextEdit,QWidget,QApplication
# import os,sys

# img = Image.open("C:\\Users\\youquan chang\\AppData\\Roaming\\Tencent\\Users\\3170147283\\QQ\\WinTemp\\RichOle\\0EGF(9%99]OU67HWG%$H}CU.png")
# print(img.size)

# class WIND(QWidget):
#     def __init__(self,parent=None):
#         super().__init__(parent)
#         self.LINE = QTextEdit(self)
#         self.resize(500,400)
#         self.LINE.resize(400,300)
#         self.LINE.move(50,50)
#         self.LINE.insertHtml("<span height='5px' width='5px'><img src='C:\\Users\\youquan chang\\AppData\\Roaming\\Tencent\\Users\\3170147283\\QQ\\WinTemp\\RichOle\\0EGF(9%99]OU67HWG%$H}CU.png'></span>")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     win = WIND()
#     win.show()
#     sys.exit(app.exec_())

# a = 5 if 6>7 else 4
# print(a)

# from ctypes import windll

# WM_APPCOMMAND = 0x0319
# APPCOMMAND_VOLUME_UP = 0x0a
# APPCOMMAND_VOLUME_DOWN = 0x09
# APPCOMMAND_MICROPHONE_VOLUME_DOWN = 25 #减小麦克风音量
# APPCOMMAND_MICROPHONE_VOLUME_UP = 26 #增加麦克风音量
# hwnd = windll.user32.GetForegroundWindow()
# for i in range(51):
#     windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_VOLUME_DOWN*0x10000)
#     windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_MICROPHONE_VOLUME_DOWN*0x10000)
# #设置初始音量为24
# for i in range(12):
#     windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_VOLUME_UP*0x10000)
#     windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,APPCOMMAND_MICROPHONE_VOLUME_UP*0x10000)

# windll.user32.PostMessageA(hwnd,WM_APPCOMMAND,0,26*0x10000)

import time

# print(time.localtime(time.time()))

print(time.localtime()[1])