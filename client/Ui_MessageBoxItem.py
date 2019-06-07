from PyQt5.QtWidgets import QFrame,QLabel,QWidget,QApplication,QTextEdit,QPushButton
from PyQt5 import QtGui
from PyQt5 import Qt as Q_t
from PIL import Image
import sys,os,re

from get_icon import getIcon


class Friend_message(QFrame):
    def __init__(self,text,parent=None):
        super().__init__(parent)
        self.text = text
        self.message_box(self.text)
        self.resize(self.text_label.width()+160,self.text_label.height()+10)
        self.text_label.move(30,5)
        self.triangle()
        self.tri.move(10,15)
        self.setStyleSheet("background-color:rgb(250,250,250);")
        self.height = self.text_label.height()+10

    def message_box(self,text):
        message = text
        pic_list = re.findall('<img.*?>',message)
        for i in pic_list:
            message = message.replace(i,'*^*%d*^*'%pic_list.index(i))
        width = 0
        height = 0
        lines = 1
        temp_width = 0
        temp_height = 0
        index = 0
        pic_index = 0
        self.have_pic = False
        self.iflines = False
        message_len = len(message)
        while True:
            temp_words = message[index]
            if temp_words == '*':
                if message[index:index+7] == ("*^*%d*^*"%pic_index) or message[index:index+8] == ("*^*%d*^*"%pic_index):
                    self.have_pic = True
                    path = pic_list[pic_index].split('\"')[1].replace('file:///','')
                    if os.path.exists(path):
                        (size,path) = resize_send_pic(path)
                        new_path = "<img src='%s'>"%path
                    else:
                        size = (30,40)
                        new_path = "<img src='%s'"%path
                    pic_list[pic_index] = new_path
                    temp_width += size[0]
                    if temp_width > 360:
                        self.iflines= True
                        lines += 1
                        temp_width = size[0]
                        height += temp_height
                    else:
                        if size[1]<=40:
                            temp_height = 30
                        else:
                            temp_height = size[1]
                    if message[index:index+7] == ("*^*%d*^*"%pic_index):
                        index += 7
                    elif message[index:index+8] == ("*^*%d*^*"%pic_index):
                        index += 8  
                    pic_index += 1
            else:
                lenth = get_width(temp_words)*10
                temp_width += lenth
                if temp_width > 360:
                    self.iflines= True
                    lines += 1
                    temp_width = lenth
                    height += temp_height
                else:
                    if not temp_height:
                        temp_height = 30
                index += 1
            if index >= message_len:
                break
        height += temp_height
        if self.iflines:#设置文本超出一行的宽高
            if self.have_pic:
                height = height + lines*7
            else:
                height = height + lines*5
            width = 360
        else:#设置文本只有一行的宽高
            height = height + 10
            width = temp_width + 20
        index = 0
        for i in pic_list:
            message = message.replace('*^*%s*^*'%index,i)
            index += 1
        self.text_label = QTextEdit(self)
        self.text_label.setHtml('''
        <p style="font-family:'黑体';font-size:12pt;line-height:1.1;">%s</p>
        '''%message)
        self.text_label.resize(width,height)
        if self.have_pic:
            self.text_label.setStyleSheet("background-color:rgb(210,210,210);border:0px;border-radius:5px;padding-left:5px;")
        else:
            self.text_label.setStyleSheet("background-color:rgb(210,210,210);border:0px;border-radius:5px;padding-left:5px;padding-top:5px;")
        self.text_label.setReadOnly(True)

    def triangle(self):
        path = os.getcwd() + '\\images\\03-22.png'
        self.tri = QLabel(self)
        self.tri.setPixmap(QtGui.QPixmap(path))
        self.tri.resize(20,15)
        self.tri.setStyleSheet("background-color:rgb(210,210,210);")
        self.tri.setScaledContents(True)

class Friend_file_message(QFrame):
    def __init__(self,text,parent=None):
        super().__init__(parent)
        self.resize(400,140)
        if os.path.exists(text):
            self.make_items(text)
        else:
            print(text)
            print("找不到文件")

    def make_items(self,text):
        icon_path,filename = getIcon(text)
        file_size = os.path.getsize(text)
        if file_size/(1024**2) > 1:
            file_size = '(' + str(round(file_size/(1024**2),2)) + ' MB)'
        else:
            file_size = '(' + str(round(file_size/(1024),2)) + ' KB)'
        #显示框
        self.main_box = QFrame(self)
        self.main_box.resize(370,130)
        self.main_box.move(10,5)
        self.main_box.setStyleSheet("border:0px solid grey;border-radius:5px;background-color:rgb(210,210,210);")
        #文件显示框
        self.file_box = QFrame(self.main_box)
        self.file_box.resize(360,80)
        self.file_box.move(5,5)
        self.file_box.setStyleSheet("border:0.5px solid grey;border-radius:0px;background-color:rgb(250,250,250);")
        #文件图标
        self.file_icon_label = QLabel(self.file_box)
        self.file_icon_label.resize(60,70)
        self.file_icon_label.move(5,5)
        self.file_icon_label.setPixmap(QtGui.QPixmap(icon_path))
        #文件名
        self.file_name_label = QLabel(self.file_box)
        self.file_name_label.resize(280,30)
        self.file_name_label.move(70,5)
        self.file_name_label.setText(filename)
        self.file_name_label.setToolTip(filename)
        self.file_name_label.setCursor(QtGui.QCursor(Q_t.Qt.PointingHandCursor))
        self.file_name_label.setFont(QtGui.QFont('宋体',12))
        self.file_name_label.setStyleSheet("border:0px solid grey;")
        #文件大小
        self.file_size_label = QLabel(self.file_box)
        self.file_size_label.resize(200,30)
        self.file_size_label.move(70,40)
        self.file_size_label.setText(file_size)
        self.file_size_label.setStyleSheet("border:0px solid grey;")

        #操作框
        self.button_box = QFrame(self.main_box)
        self.button_box.resize(360,40)
        self.button_box.move(5,85)
        self.button_box.setStyleSheet("border:0.5px solid grey;border-top:0px;border-radius:0px;background-color:rgb(250,250,250);")
        #打开文件
        self.open_file_button = QPushButton(self.button_box)
        self.open_file_button.resize(40,20)
        self.open_file_button.move(219,10)
        self.open_file_button.setText('打开')
        self.open_file_button.setCursor(QtGui.QCursor(Q_t.Qt.PointingHandCursor))
        self.open_file_button.setStyleSheet("border:0px solid grey;color:blue;")
        self.open_file_button.clicked.connect(lambda: self.open_file(text))
        #打开文件夹
        self.open_dir_button = QPushButton(self.button_box)
        self.open_dir_button.resize(100,20)
        self.open_dir_button.move(259,10)
        self.open_dir_button.setText('打开文件夹')
        self.open_dir_button.setCursor(QtGui.QCursor(Q_t.Qt.PointingHandCursor))
        self.open_dir_button.setStyleSheet("border:0px solid grey;color:blue;")
        self.open_dir_button.clicked.connect(lambda: self.open_dir(text))

    def open_file(self,text):
        text = 'file:' + text
        Q_t.QDesktopServices.openUrl(Q_t.QUrl(text))

    def open_dir(self,text):
        print(text)
        dir_path = '/'.join(text.split('/')[0:-1])
        print(dir_path)
        dir_path = 'file:' + dir_path
        Q_t.QDesktopServices.openUrl(Q_t.QUrl(dir_path,Q_t.QUrl.TolerantMode))

class Mine_message(QFrame):
    def __init__(self,text,parent=None):
        super().__init__(parent)
        self.text = text
        self.message_box(self.text)
        self.resize(self.text_label.width()+160,self.text_label.height())
        if self.iflines:
            self.text_label.move(170,5)
        else:
            self.text_label.move(self.locate,5)
        self.triangle()
        self.tri.move(530,10)
        self.setStyleSheet("background-color:rgb(250,250,250);")
        self.height = self.text_label.height()+40
        
    def message_box(self,text):
        message = text
        pic_list = re.findall('<img.*?>',message)
        index = 0
        for i in pic_list:
            message = message.replace(i,'*^*%d*^*'%index,1)
            index += 1
        width = 0
        height = 0
        lines = 1
        temp_width = 0
        temp_height = 0
        index = 0
        pic_index = 0
        self.have_pic = False
        self.iflines = False
        message_len = len(message)
        while True:
            temp_words = message[index]
            if temp_words == '*':
                if message[index:index+7] == ("*^*%d*^*"%pic_index) or message[index:index+8] == ("*^*%d*^*"%pic_index):
                    self.have_pic = True
                    path = pic_list[pic_index].split('\"')[1].replace('file:///','')
                    if os.path.exists(path):
                        (size,path) = resize_send_pic(path)
                        new_path = "<img src='%s'>"%path
                    else:
                        size = (30,40)
                        new_path = "<img src='%s'"%path
                    pic_list[pic_index] = new_path
                    temp_width += size[0]
                    if temp_width > 360:
                        self.iflines= True
                        lines += 1
                        temp_width = size[0]
                        height += temp_height
                    else:
                        if size[1]<=40:
                            temp_height = 30
                        else:
                            temp_height = size[1]
                    if message[index:index+7] == ("*^*%d*^*"%pic_index):
                        index += 7
                    elif message[index:index+8] == ("*^*%d*^*"%pic_index):
                        index += 8  
                    pic_index += 1
            else:
                lenth = get_width(temp_words)*10
                temp_width += lenth
                if temp_width > 360:
                    self.iflines= True
                    lines += 1
                    temp_width = lenth
                    height += temp_height
                else:
                    if not temp_height:
                        temp_height = 30
                index += 1
            if index >= message_len:
                break
        height += temp_height
        if self.iflines:#设置文本超出一行的宽高
            if self.have_pic:
                height = height + lines*7
            else:
                height = height + lines*5
            width = 360
        else:#设置文本只有一行的宽高
            height = height + 10
            width = temp_width + 20
        index = 0
        for i in pic_list:
            message = message.replace('*^*%s*^*'%index,i)
            index += 1
        self.text_label = QTextEdit(self)
        self.text_label.setHtml('''
        <p style="font-family:'黑体';font-size:12pt;line-height:1.2;">%s</p>
        '''%message)
        self.text_label.resize(width,height)
        if self.have_pic:
            self.text_label.setStyleSheet("background-color:rgb(240,240,240);border:0px;border-radius:5px;padding-left:5px;")
        else:
            self.text_label.setStyleSheet("background-color:rgb(240,240,240);border:0px;border-radius:5px;padding-left:5px;padding-top:5px;")           
        self.text_label.setReadOnly(True)
        self.locate = 531 - width 

    def triangle(self):
        path = os.getcwd() + '\\images\\03-23.png'
        self.tri = QLabel(self)
        self.tri.setPixmap(QtGui.QPixmap(path))
        self.tri.resize(20,15)
        self.tri.setStyleSheet("background-color:rgb(210,210,210);")
        self.tri.setScaledContents(True)

class My_file_message(QFrame):
    def __init__(self,text,parent=None):
        super().__init__(parent)
        self.resize(400,140)
        if os.path.exists(text):
            self.make_items(text)
        else:
            pass

    def make_items(self,text):
        icon_path,filename = getIcon(text)
        file_size = os.path.getsize(text)
        if file_size/(1024**2) > 1:
            file_size = '(' + str(round(file_size/(1024**2),2)) + ' MB)'
        else:
            file_size = '(' + str(round(file_size/(1024),2)) + ' KB)'
        #显示框
        self.main_box = QFrame(self)
        self.main_box.resize(370,130)
        self.main_box.move(180,5)
        self.main_box.setStyleSheet("border-radius:5px;background-color:rgb(240,240,240);")
        #文件显示框
        self.file_box = QFrame(self.main_box)
        self.file_box.resize(360,80)
        self.file_box.move(5,5)
        self.file_box.setStyleSheet("border:0.5px solid grey;border-radius:0px;background-color:rgb(250,250,250);")
        #文件图标
        self.file_icon_label = QLabel(self.file_box)
        self.file_icon_label.resize(60,70)
        self.file_icon_label.move(5,5)
        self.file_icon_label.setPixmap(QtGui.QPixmap(icon_path))
        #文件名
        self.file_name_label = QLabel(self.file_box)
        self.file_name_label.resize(280,30)
        self.file_name_label.move(70,5)
        self.file_name_label.setText(filename)
        self.file_name_label.setToolTip(filename)
        self.file_name_label.setCursor(QtGui.QCursor(Q_t.Qt.PointingHandCursor))
        self.file_name_label.setFont(QtGui.QFont('宋体',12))
        self.file_name_label.setStyleSheet("border:0px solid grey;")
        #文件大小
        self.file_size_label = QLabel(self.file_box)
        self.file_size_label.resize(200,30)
        self.file_size_label.move(70,40)
        self.file_size_label.setText(file_size)
        self.file_size_label.setStyleSheet("border:0px solid grey;")

        #操作框
        self.button_box = QFrame(self.main_box)
        self.button_box.resize(360,40)
        self.button_box.move(5,85)
        self.button_box.setStyleSheet("border:0.5px solid grey;border-top:0px;border-radius:0px;background-color:rgb(250,250,250);")
        #打开文件
        self.open_file_button = QPushButton(self.button_box)
        self.open_file_button.resize(40,20)
        self.open_file_button.move(219,10)
        self.open_file_button.setText('打开')
        self.open_file_button.setStyleSheet("border:0px solid grey;color:blue;")
        self.open_file_button.clicked.connect(lambda: self.open_file(text))
        #打开文件夹
        self.open_dir_button = QPushButton(self.button_box)
        self.open_dir_button.resize(100,20)
        self.open_dir_button.move(259,10)
        self.open_dir_button.setText('打开文件夹')
        self.open_dir_button.setStyleSheet("border:0px solid grey;color:blue;")
        self.open_dir_button.clicked.connect(lambda: self.open_dir(text))

    def open_file(self,text):
        text = 'file:' + text
        Q_t.QDesktopServices.openUrl(Q_t.QUrl(text))

    def open_dir(self,text):
        dir_path = '/'.join(text.split('/')[0:-1])
        dir_path = 'file:' + dir_path
        Q_t.QDesktopServices.openUrl(Q_t.QUrl(dir_path,Q_t.QUrl.TolerantMode))

def get_width(o):#获取指定字符宽度
    """Return the screen column width for unicode ordinal o."""
    widths = [
    (126,  1), (159,  0), (687,   1), (710,  0), (711,  1),
    (727,  0), (733,  1), (879,   0), (1154, 1), (1161, 0),
    (4347,  1), (4447,  2), (7467,  1), (7521, 0), (8369, 1),
    (8426,  0), (9000,  1), (9002,  2), (11021, 1), (12350, 2),
    (12351, 1), (12438, 2), (12442,  0), (19893, 2), (19967, 1),
    (55203, 2), (63743, 1), (64106,  2), (65039, 1), (65059, 0),
    (65131, 2), (65279, 1), (65376,  2), (65500, 1), (65510, 2),
    (120831, 1), (262141, 2), (1114109, 1),
    ]
    if o == 0xe or o == 0xf:
        return 0
    for num, wid in widths:
        if ord(o) <= num:
            return wid
    return 1

def resize_send_pic(path):#调整发送的图片大小和路径
    print("发送的图片路径:",path)
    img = Image.open(path)
    new_path = path
    (x,y) = img.size #read image size
    (x_s,y_s)=(x,y)
    if x > 100:
        # print(x,y)
        x_s = x*0.8 #define standard width
        if x_s > 360:
            x_s = 360
            y_s = y * x_s / x
        else:
            y_s = y * x_s / x #calc height based on standard width
        out = img.resize((int(x_s),int(y_s)),Image.ANTIALIAS) #resize image with high-quality
        try:
            new_path = "temp_info/resized_send_pic/" + path.split('\\')[-1]
            out.save(new_path)
        except Exception:
            new_path = "temp_info/resized_send_pic/" + path.split('/')[-1]
            out.save(new_path)
        # print(x_s,y_s)
        return (x_s,y_s),new_path
    return (x,y),new_path

def resize_received_pic(path):
    img = Image.open(path)
    new_path = path
    (x,y) = img.size #read image size
    (x_s,y_s)=(x,y)
    if x > 100:
        # print(x,y)
        x_s = x*0.8 #define standard width
        if x_s > 360:
            x_s = 360
            y_s = y * x_s / x
        else:
            y_s = y * x_s / x #calc height based on standard width
        out = img.resize((int(x_s),int(y_s)),Image.ANTIALIAS) #resize image with high-quality
        new_path = "temp_info/resized_received_pic/" + path.split('\\')[-1]
        out.save(new_path)
        # print(x_s,y_s)
        return (x_s,y_s),new_path
    return (x,y),new_path


# class Friend_message(QFrame):
#     def __init__(self,text,parent=None):
#         super().__init__(parent)
#         self.text = text
#         self.message_box(self.text)
#         self.resize(self.text_label.width()+160,self.text_label.height()+10)
#         self.text_label.move(30,5)
#         self.triangle()
#         self.tri.move(10,15)
#         self.setStyleSheet("background-color:rgb(250,250,250);")
#         self.height = self.text_label.height()+10

#     def message_box(self,text):
#         message = ''
#         temp_line = ''
#         width = 0
#         height = 0
#         temp_width = 0
#         lines = 1
#         for i in text:
#             lenth = get_width(i)*10
#             temp_width += lenth
#             temp_line += i
#             if temp_width >= 360:
#                 message += temp_line
#                 message += '\n'
#                 temp_width = 0
#                 temp_line = ''
#                 lines += 1
#         else:
#             message += temp_line
#             if lines > 1:
#                 width = 380
#             else:
#                 width = temp_width+20
#             if lines <= 1:
#                 height = 40
#             else:
#                 height = lines*30
#         self.text_label = QTextEdit(self)
#         self.text_label.setHtml(message)
#         self.text_label.resize(width,height)
#         self.text_label.setFont(QtGui.QFont("黑体",12))
#         self.text_label.setStyleSheet("background-color:rgb(210,210,210);border-radius:10px;padding:4,4,4,4;")
#         self.text_label.setReadOnly(True)

#     def triangle(self):
#         path = os.getcwd() + '\\images\\03-22.png'
#         self.tri = QLabel(self)
#         self.tri.setPixmap(QtGui.QPixmap(path))
#         self.tri.resize(20,15)
#         self.tri.setStyleSheet("background-color:rgb(210,210,210);")
#         self.tri.setScaledContents(True)

