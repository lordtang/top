import sys,os
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QScrollBar,
QTableWidget,QAbstractItemView,QTableWidgetItem,QTextEdit,
QPushButton,QFrame,QLineEdit,QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5 import QtGui,QtCore
from threading import Thread
from socket import *
from datetime import datetime,date
import time
import re
from struct import Struct


from Ui_ChatWin import Ui_ChatWin
from Ui_FriendInfo import FriendFrame
from CallFriendRequestWin import FrirenRequestWin
from CallPresonInfo import PersonInfo
from CallExpressionForm import ExpressionForm
from CallVoiceChatWin import VoiceChatWin
from CallVideoChatWin import VideoChatWin
from CallFileSR import FileSRWin
from CallAddWin import AddWin
from Ui_MyTableWidget import MyTbaleWidget,MyLabel
from Ui_AddfridItem import Friend_info_item
from Ui_MessageBoxItem import *
from settings import expression_dic
from get_icon import getIcon
from media import VideoServer,VideoClient,AudioClient,AudioServer

class ChatWin(QWidget, Ui_ChatWin):
    def __init__(self,client,my_info=None,friends_info=None,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.client = client
        self.my_info = my_info
        print(self.my_info)
        self.friends_info = friends_info
        print(self.friends_info)
        self.server_addr = ('176.209.106.8', 8080)
        # self.server_addr = ('192.168.199.195', 8080)
        #新建发送消息套接字
        self.send_addr = ('0.0.0.0',8081)
        self.send_sockfd = socket(AF_INET,SOCK_DGRAM)
        self.send_sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.send_sockfd.bind(self.send_addr)
        #接收消息套接字地址
        self.recv_addr = ('0.0.0.0',8082)
        self.recv_sockfd = socket(AF_INET,SOCK_DGRAM)
        self.recv_sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.recv_sockfd.bind(self.recv_addr)
        online = '10086' + ' ' + self.my_info[0]
        self.recv_sockfd.sendto(online.encode(),self.server_addr)
        #心跳包套接字地址
        self.heart_beat_addr = ('0.0.0.0',8083)

        #初始我的头像
        self.my_icon = QtGui.QIcon()
        self.my_icon.addPixmap(QtGui.QPixmap(self.my_info[5]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_10.setIcon(self.my_icon)
        #初始设置
        self.setWindowFlags(Qt.FramelessWindowHint)#设置无边框
        self.pushButton_5.hide()
        self.pushButton_6.hide()
        self.label_3.hide()
        self.friends_item_info = {} #用于存储请求加好友后接收到好友消息的字典
        self.menuisshow = False   #菜单是否弹出
        self.isviewed = False     #消息是否查看
        self.file_is_sending = False  #用于判断文件是否正在传输
        self.set_process_value = QLineEdit(self)   #用于设置文件传输进度
        self.set_process_value.hide()
        self.reshow_msgbox_signal = QLineEdit(self)  #用于接收到消息后刷新消息框
        self.reshow_msgbox_signal.hide()
        self.reshow_temp_list_signal = QLineEdit(self) #用于接收到消息后刷新临时会话列表
        self.reshow_temp_list_signal.hide()
        self.thread_show_file_sr_signal = QLineEdit(self) #用于接收消息后显示文件传输窗口
        self.thread_show_file_sr_signal.hide()

        #视频聊天
        self.thread_show_video_chat_win = QLineEdit(self) #用于接收消息后显示视频聊天窗口
        self.thread_show_video_chat_win.hide()
        self.aimuser_agree_vchat = QLineEdit(self) #对方接受视频请求的处理信号
        self.aimuser_agree_vchat.hide()
        self.interupt_vchat = QLineEdit(self) #终止视频的处理信号
        self.interupt_vchat.hide()
        #语音聊天
        self.thread_show_voice_chat_win = QLineEdit(self) #用于接收消息后显示语音聊天窗口
        self.thread_show_voice_chat_win.hide()
        self.aimuser_agree_achat = QLineEdit(self) #对方接收语音请求的处理信号
        self.aimuser_agree_achat.hide()
        self.interupt_achat = QLineEdit(self) #终止语音的处理信号
        self.interupt_achat.hide()
        #添加好友
        self.recv_find_friends_rsp = QLineEdit(self) #收到查找好友的信息
        self.recv_find_friends_rsp.hide()
        self.show_friend_item = QLineEdit(self) #显示好友Item
        self.show_friend_item.hide()
        self.friend_request_signal = QLineEdit(self) #收到添加好友请求的信号
        self.friend_request_signal.hide()
        self.reshow_friends_list_siganl = QLineEdit(self) #好友添加成功，刷新好友列表
        self.reshow_friends_list_siganl.hide()
        self.reshow_friends_list_siganl2 = QLineEdit(self)
        self.reshow_friends_list_siganl2.hide()

        self.file_s_info = [] #用于存储发送文件窗口的相关信息
        self.file_r_info = [] #用于存储接收消息后需要显示的文件窗口的相关信息
        self.new_table = MyTbaleWidget(self)  #临时聊天列表
        self.new_table.hide()
        self.pic_waitting_tobesend = {}  #用于保存需要被发送但还没发送的图片
        self.file_waitting_tobesend = {}  #用于保存需要被发送但还没发送的文件
        self.current_row = 0
        #触发事件
        self.pushButton.clicked.connect(self.create_temp_list)     #点击消息按钮生成临时会话列表
        self.pushButton_2.clicked.connect(self.create_friend_list) #点击联系人按钮生成好友列表
        self.pushButton_4.clicked.connect(self.open_add_win) #点击按钮打开添加窗口
        self.pushButton_5.clicked.connect(self.show_person_info)
        self.pushButton_7.clicked.connect(self.menu_show_close)
        self.new_table.cellClicked.connect(self.handle_newitem_click)  #响应点击newtalbe的Item事件
        self.new_table.cellEntered.connect(self.handle_cell_enter)     #响应鼠标滑入某一行
        self.tableWidget_2.cellClicked.connect(self.handle_item_click) #响应点击tableWidget2的Item事件
        self.pushButton_9.clicked.connect(lambda: self.video_chat("request",self.send_sockfd,self.name_count[1],'',self.server_addr,self.reshow_msgbox_signal)) #发起视频聊天
        self.aimuser_agree_vchat.textChanged.connect(self.handle_aimagree_vchat) #开始视频聊天
        self.interupt_vchat.textChanged.connect(self.handle_vchat_interupt) #视频聊天中断
        self.pushButton_14.clicked.connect(lambda: self.voice_chat('request',self.send_sockfd,self.my_info[0],self.name_count[1],'',self.server_addr,self.reshow_msgbox_signal))  #发起语音聊天
        self.aimuser_agree_achat.textChanged.connect(self.handle_aimagree_achat) #开始语音聊天
        self.interupt_achat.textChanged.connect(self.handle_achat_interupt) #语音聊天中断
        self.pushButton_15.clicked.connect(self.send_message) #点击发送键发送消息
        self.pushButton_16.clicked.connect(self.open_expression)  #打开表情窗口
        self.pushButton_17.clicked.connect(self.open_img)  #发送图片
        self.pushButton_18.clicked.connect(self.open_file)  #发送文件窗口
        self.reshow_msgbox_signal.textChanged.connect(self.reshow_msgbox) #重绘消息显示列表
        self.reshow_temp_list_signal.textChanged.connect(self.create_temp_list) #重绘临时会话列表
        self.thread_show_file_sr_signal.textChanged.connect(self.thread_show_file_sr) #接收文件窗口
        self.thread_show_video_chat_win.textChanged.connect(self.response_video) #收到消息触发信号显示视频聊天窗口
        self.thread_show_voice_chat_win.textChanged.connect(self.response_voice) #收到消息触发信号显示语音聊天窗口
        self.recv_find_friends_rsp.textChanged.connect(lambda: self.start_recv_friends_info(self.recv_find_friends_rsp.text(),self.add_win))
        self.show_friend_item.textChanged.connect(self.show_friends_item) #显示好友Item
        self.friend_request_signal.textChanged.connect(self.handle_friend_request) #处理好友请求
        self.reshow_friends_list_siganl.textChanged.connect(self.recv_show_friends_list) #接收好友列表
        self.reshow_friends_list_siganl2.textChanged.connect(self.recv_show_friends_list)
        self.set_process_value.textChanged.connect(self.set_process) #设置进度条进度值
        self.tableWidget.verticalScrollBar().setVisible(False)
        self.textEdit.textChanged.connect(self.press_enter_send)    #按Enter键发送消息
        self.create_temp_list()  #创建临时聊天列表
        try:
            self.name_count = self.new_table.item(0,4).text().split(' ')
            self.label_2.setText(self.name_count[0])
            self.create_message_item(self.name_count[1])
        except Exception:
            pass
        self.start_child_thread()
        #气泡设置
        self.pushButton.setToolTip("聊天")
        self.pushButton_2.setToolTip("好友")
        self.pushButton_3.setToolTip("群聊")
        self.pushButton_4.setToolTip("添加")
        self.pushButton_5.setToolTip("个人信息")
        self.pushButton_6.setToolTip("注销")
        self.pushButton_7.setToolTip("菜单")
        
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
        try:
            if self.expression_form.isVisible():
                self.expression_form.hide()
                self.textEdit.setFocus()
        except Exception:
            pass

    def mouseMoveEvent(self, QMouseEvent):
        try:
            if Qt.LeftButton and self.m_flag:  
                self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
                QMouseEvent.accept()
        except AttributeError:
            pass
        try:
            self.file_sr_win.setGeometry(self.geometry().x()+1050,self.geometry().y(),350,700)
        except:
            pass

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False

    def create_temp_list(self):#生成临时会话列表
        self.new_table.clear()
        self.isviewed = True
        self.label_3.hide()
        self.tableWidget_2.hide()
        self.new_table.show()
        try:
            if self.friend_info_frame.isVisible():
                self.friend_info_frame.close()
        except AttributeError:
            pass
        self.new_table.verticalScrollBar().setSliderPosition(0)
        temp_con_list = []
        path1 = 'Top files\\' + self.my_info[0] + '\\temp_conversation.txt'
        with open(path1,'r') as f:
            for i in f.readlines():
                if i.rstrip() != self.my_info[0]:
                    temp_con_list.append(i)
        self.new_table.setRowCount(len(temp_con_list)*2)
        self.new_table.setColumnCount(5)
        self.new_table.setFocusPolicy(Qt.NoFocus)
        self.new_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.new_table.setStyleSheet('''
        QTableWidget::item:selected {background-color: rgb(220, 220, 220)}
        QTableWidget{border:0px;background-color:transparent};
        ''')
        self.new_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.new_table.setShowGrid(False)
        self.new_table.setIconSize(QtCore.QSize(60,60))
        self.new_table.setColumnWidth(0,70)
        self.new_table.setColumnWidth(1,100)
        self.new_table.setColumnWidth(2,70)
        self.new_table.setColumnWidth(3,0)
        self.new_table.setColumnWidth(4,0)
        self.new_table.setContentsMargins(10,0,10,0)
        self.new_table.verticalHeader().setVisible(False)
        self.new_table.horizontalHeader().setVisible(False)
        count = 0
        path2 = 'Top files\\' + self.my_info[0] + '\\temp_message.txt'
        path3 = 'Top files\\' + self.my_info[0] + '\\message_record.txt'
        for i in temp_con_list:
            i = i.rstrip()
            self.new_table.setRowHeight(count,45)
            self.new_table.setRowHeight(count+1,45)
            head_pic = QLabel()
            head_pic.setPixmap(QtGui.QPixmap(self.friends_info[i][1]))
            head_pic.setScaledContents(True)
            head_pic.setStyleSheet('''border-top:15px solid transparent;border-bottom:15px solid transparent;
            border-left:5px solid transparent;border-right:5px solid transparent;''')
            self.new_table.setCellWidget(count,0,head_pic)
            self.new_table.setSpan(count,0,2,1)
            cell = self.new_table.cellWidget(count,0)
            cell.resize(45,45)

            last_message = []
            f = open(path2)
            for j in f.readlines():
                if j.split(' ')[1] == i or j.split(' ')[2] == i:
                    last_message = j.split(' ')
            f.close()
            if not last_message:
                f = open(path3)
                for k in f.readlines():
                    if k.split(' ')[1] == i or k.split(' ')[2] == i:
                        last_message = k.split(' ')
            f.close()
            fname = self.friends_info[i][0]
            text=''
            for l in last_message[3:-2]:
                text += l
            text = self.handle_last_message(text)
            now = str(datetime.now()).split(' ')
            time = ''
            try:
                if last_message[-2] == now[0]:
                    time = last_message[-1][0:5]
                else:
                    time = last_message[-2][2:]
                    time = time.replace('-','/')
            except IndexError:
                pass
            
            #设置昵称和消息
            n_label = MyLabel()
            n_label.setText(fname)
            n_label.setAlignment(Qt.AlignTop)
            n_label.setStyleSheet("border-top:8px solid transparent;")
            n_label.setMargin(5)
            n_label.setFont(QtGui.QFont('黑体',12,10))
            t_label = MyLabel()
            t_label.setText('\n'+'\n'+'\n'+text)
            t_label.setMargin(5)
            t_label.setStyleSheet("color:grey;")
            self.new_table.setCellWidget(count,1,n_label)
            self.new_table.setCellWidget(count+1,1,t_label)
            self.new_table.setSpan(count,1,2,1)

            date_time = MyLabel()
            date_time.setText(time)
            date_time.setAlignment(Qt.AlignTop|Qt.AlignRight)
            date_time.setStyleSheet("border-top:8px solid transparent;")
            self.new_table.setCellWidget(count,2,date_time)
            self.new_table.setSpan(count,2,2,1)

            timetamp1 = ''
            try:
                timetamp1 = QTableWidgetItem(last_message[-2]+' '+last_message[-1])
                self.new_table.setItem(count,3,timetamp1)
            except IndexError:
                pass
            timetamp2 = ''
            try:
                timetamp2 = QTableWidgetItem(last_message[-2]+' '+last_message[-1])
                self.new_table.setItem(count+1,3,timetamp2)
            except IndexError:
                pass
            self.new_table.setSpan(count,3,2,1)

            info = QTableWidgetItem(self.friends_info[i][0]+' '+i)
            self.new_table.setItem(count,4,info)
            self.new_table.setSpan(count,4,2,1)

            count += 2
        self.new_table.sortItems(3,QtCore.Qt.DescendingOrder)
        self.new_table.move(90,80)
        self.new_table.resize(241,620)

    def handle_last_message(self,message):#处理最后一条消息
        pic_list = re.findall('<img.*?>',message)
        exp_dic = {}
        picture_dic = {}
        for i in pic_list:
            img_name = i.split('\"')[1].split('/')[-1]
            if img_name in expression_dic:
                exp_dic[i] = expression_dic[img_name]
            else:
                picture_dic[i] = "[图片]"
        for i in exp_dic:
            message = message.replace(i,exp_dic[i])
        for i in picture_dic:
            message = message.replace(i,'[图片]')
        return message

    def create_friend_list(self):#生成好友列表
        self.new_table.hide()
        self.tableWidget_2.show()
        leng = 0
        for i in self.friends_info:
            leng += 1
        self.tableWidget_2.setRowCount(leng)
        self.tableWidget_2.setColumnCount(2)
        self.tableWidget_2.setFocusPolicy(Qt.NoFocus)
        self.tableWidget_2.setStyleSheet('''QTableWidget::item:selected {background-color: rgb(220, 220, 220)}
        QTableWidget::item:hover {background-color: rgb(235, 235, 235)}
        ''')
        self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_2.setShowGrid(False)
        self.tableWidget_2.setIconSize(QtCore.QSize(50,50))
        self.tableWidget_2.setColumnWidth(0,240)
        self.tableWidget_2.setColumnWidth(1,0)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tableWidget_2.horizontalHeader().setVisible(False)

        count = 0
        for i in self.friends_info:
            self.tableWidget_2.setRowHeight(count,70)
            head_pic = QTableWidgetItem(self.friends_info[i][0])
            icon = QtGui.QIcon(self.friends_info[i][1])
            head_pic.setIcon(QtGui.QIcon(icon))
            head_pic.setFont(QtGui.QFont("Times",10,QtGui.QFont.Black))
            self.tableWidget_2.setItem(count,0,head_pic)
            order = QTableWidgetItem(self.friends_info[i][0]+' '+i)
            self.tableWidget_2.setItem(count,1,order)
            count += 1
        self.tableWidget_2.sortItems(1,QtCore.Qt.AscendingOrder)

    def handle_item_click(self,row):#点击Table的响应函数
        try:
            if self.friend_info_frame.isVisible():
                self.friend_info_frame.close()
        except AttributeError:
            pass
        info = self.tableWidget_2.item(row,1).text()
        self.name_count = info.split(' ')
        self.label_2.setText(self.name_count[0])
        friend_info = []
        friend_info.append(self.name_count[1])
        for i in self.friends_info:
            if i == self.name_count[1]:
                friend_info.extend(self.friends_info[i])
        print(friend_info)
        self.show_friend_info(self.my_info[0],friend_info)

    def handle_newitem_click(self,row):#响应NewTable点击
        info = self.new_table.item(row,4).text()
        self.name_count = info.split(' ')
        self.label_2.setText(self.name_count[0])
        self.invert_message_status(self.name_count[1])
        self.create_message_item(self.name_count[1])

    def handle_cell_enter(self,row):#响应鼠标进入NewTable某一行
        try:
            self.before_row = self.current_row
            cell1 = self.new_table.cellWidget(self.before_row,0)
            cell1.setStyleSheet('''background-color:transparent;border-top:15px solid transparent;border-bottom:15px solid transparent;
            border-left:5px solid transparent;border-right:5px solid transparent;''')
            cell2 = self.new_table.cellWidget(self.before_row,1)
            cell2.setStyleSheet("background-color:transparent;border-top:8px solid transparent;")
            cell3 = self.new_table.cellWidget(self.before_row,2)
            cell3.setStyleSheet("background-color:transparent;border-top:8px solid transparent;")
        except Exception:
            pass
        self.current_row = row
        cell4 = self.new_table.cellWidget(row,0)
        cell4.setStyleSheet('''background-color:rgb(235,235,235);border-top:15px solid transparent;border-bottom:15px solid transparent;
            border-left:5px solid transparent;border-right:5px solid transparent;''')
        cell5 = self.new_table.cellWidget(row,1)
        cell5.setStyleSheet("background-color:rgb(235,235,235);border-top:8px solid transparent;")
        cell6 = self.new_table.cellWidget(row,2)
        cell6.setStyleSheet("background-color:rgb(235,235,235);border-top:8px solid transparent;")
    
    def send_message(self):#发消息
        myID = self.my_info[0]
        aimID = self.name_count[1]
        text = self.textEdit.toHtml()
        text = re.findall('text-indent:0px;">.*</p',text)
        text = text[0]
        text = text.replace('text-indent:0px;">','')
        text = text.replace('</p','')
        text = text.rstrip()
        msg = '036'+ ' ' + self.my_info[0] + ' ' + self.name_count[1] + ' ' + text + ' ' + str(datetime.now())
        while True:
            try:
                path = 'Top files\\' + self.my_info[0] + '\\message_record.txt' 
                with open(path,'at') as f:
                    f.write(msg + '\n')
                f.close()
                break
            except Exception:
                pass
        (text,old_path_list,new_path_list,havepic) = self.judge_onlytext(text,self.my_info[0],self.name_count[1])
        if havepic:
            self.client.send_message(self.send_sockfd,myID,aimID,text)
            print("text:   ",text)
            self.send_pic_send_request(self.send_sockfd,old_path_list,new_path_list,myID,aimID)
        else:
            self.client.send_message(self.send_sockfd,myID,aimID,text)
        self.textEdit.setText('')
        self.create_message_item(self.name_count[1])
        self.create_temp_list()

    def press_enter_send(self):#按Enter键发送消息
        try:
            if self.textEdit.toPlainText()[-1] == '\n':
                myID = self.my_info[0]
                aimID = self.name_count[1]
                text = self.textEdit.toPlainText().rstrip()
                msg = '036'+ ' ' + self.my_info[0] + ' ' + self.name_count[1] + ' ' + text + ' ' + str(datetime.now())
                while True:
                    try:
                        path = 'Top files\\' + self.my_info[0] + '\\message_record.txt'
                        with open(path,'at') as f:
                            f.write(msg + '\n')
                        f.close()
                        break
                    except Exception:
                        pass
                self.client.send_message(self.send_sockfd,myID,aimID,text)
                self.textEdit.setText('')
                self.create_message_item(self.name_count[1])
                self.create_temp_list()
            # else:#用一个备用textEdit同步

        except IndexError:
            pass

    def judge_onlytext(self,text,myID,aimID):#判断发送的消息中是否带有图片
        pic_list = re.findall('<img.*?>',text)
        old_path_list = []
        new_path_list = []
        for i in pic_list:
            img_name = i.split('\"')[1].split('/')[-1]
            if img_name not in expression_dic:
                old_path_list.append(i)
                suffix = img_name.split('.')[-1]
                new_path = '<img src="Top files\\%d\\image\\C2C\\%s.%s"/>'%(int(aimID),
                str(myID)+str(aimID)+str(datetime.now().strftime("%Y%m%d%H%M%S%f")),suffix)
                new_path_list.append(new_path)
        if old_path_list:
            index = 0
            for i in old_path_list:
                text_handled = text.replace(i,new_path_list[index],1)
                index += 1
            return text_handled,old_path_list,new_path_list,True
        else:
            return text,[],[],False

    def send_pic_send_request(self,udp_sockfd,old_path_list,new_path_list,myID,aimID):#发送发图片请求
        index = 0
        for i in old_path_list:
            local_path = i.split('\"')[1].replace('file:///','')
            result_path = new_path_list[index].split('\"')[1]
            self.pic_waitting_tobesend[result_path] = local_path
            self.client.send_pic_request(self.send_sockfd,myID,aimID,result_path)
            index += 1

    def send_pic(self,content,myID,aimID):#发送图片
        self.client.handle_file(content,myID)
        filename = content.split('*^$*#%*')[2].split('\\')[-1]
        msg = '0651' + ' ' + myID + ' ' + aimID + ' ' + filename
        self.send_sockfd.sendto(msg.encode(),self.server_addr)

    def open_img(self):#打开图片
        fpath,_ = QFileDialog.getOpenFileName(self,'Open file','c:\\',"Image files (*.bmp *.jpg *.png *.tif *.gif *.pcx *.tga *.exif *.fpx *.svg\
             *.psd *.cdr *.pcd *.dxf *.ufo *.eps *.ai *.raw *.WMF *.webp)")
        print(fpath)
        if fpath:
            self.textEdit.insertHtml('<img src="%s">'%fpath)
        self.textEdit.setFocus()

    def start_pic_send_thread(self,local_path,result_path,myID,aimID):#启动发送图片线程
        content = 'put' + '*^$*#%*' + local_path + '*^$*#%*' + result_path
        send_pic = Thread(target=self.send_pic,args=(content,myID,aimID))
        send_pic.setDaemon(True)
        send_pic.start()

    def recv_pic(self,content,myID):#接收图片
        self.client.handle_file(content,myID)
        print("图片接收完毕")
        if self.reshow_msgbox_signal.text() == '1':
            self.reshow_msgbox_signal.setText('2')
        else:
            self.reshow_msgbox_signal.setText('1')

    def start_pic_recv_thread(self,filename,myID):#启动接收图片线程
        content = 'get' + '*^$*#%*' + filename
        recv_pic = Thread(target=self.recv_pic,args=(content,myID))
        recv_pic.setDaemon(True)
        recv_pic.start()

    def open_file(self):#打开文件
        fpath,_ = QFileDialog.getOpenFileName(self,'Open file','c:\\')
        print(fpath)
        if fpath:
            file_size = os.path.getsize(fpath)
            location = (self.geometry().x()+1050,self.geometry().y())
            icon_path,filename = getIcon(fpath)
            self.client.send_file_request(self.send_sockfd,self.my_info[0],self.name_count[1],filename,file_size)
            self.file_s_info = [location,icon_path,filename,file_size,self.my_info[0],self.name_count[1]]
            self.show_file_sr(location,icon_path,filename,file_size,'send')
            self.start_file_send_thread(fpath,filename,self.my_info[0],self.name_count[1],self.file_sr_win,self.send_sockfd,self.set_process_value)

    def show_file_sr(self,location,icon_path,filename,file_size,mode):#打开文件收发窗口
        self.file_sr_win = FileSRWin(location,icon_path,filename,file_size,mode)
        if mode == 'send':
            self.file_sr_win.RecvButton.hide()
            self.file_sr_win.CancelButton.clicked.connect(lambda: self.interrupt_trans(self.file_s_info[4],self.file_s_info[2]))
        else:
            self.file_sr_win.RecvButton.clicked.connect(lambda: self.agree_trans(self.file_r_info[4],self.file_r_info[5],self.file_r_info[6]))
            self.file_sr_win.CancelButton.clicked.connect(lambda: self.interrupt_trans(self.file_r_info[5],self.file_r_info[6]))
        self.file_sr_win.show()

    def send_file(self,content,myID,aimID,file_win,send_sockfd,process_value):#发送文件
        self.file_is_sending = True
        self.client.handle_normal_file(content,myID,file_win,process_value)
        self.file_is_sending = False
        # 文件发送完毕，在消息文件中添加一条消息
        if file_win.interupt_flag.text() == 'False':
            localpath = content.split('*^$*#%*')[1]
            message_record_path = "Top files\\%s\\message_record.txt"%myID
            while True:    
                try:
                    with open(message_record_path,'at') as f:
                        time_tamp = datetime.now()
                        msg = '038 ' + myID + ' ' + aimID + ' ' + localpath + ' ' + str(time_tamp) + '\n'
                        f.write(msg)
                    f.close()
                    break
                except Exception:
                    continue
            filename = content.split('*^$*#%*')[2]
            msg = '06411' + ' ' + myID + ' ' + aimID + ' ' + filename
            send_sockfd.sendto(msg.encode(),self.server_addr)
            file_win.close()
            # 消息发送完毕，重绘消息显示框
            if self.reshow_msgbox_signal.text() == '1':
                self.reshow_msgbox_signal.setText('2')
            else:
                self.reshow_msgbox_signal.setText('1')

    def set_process(self):#设置文件收发窗口进度条进度值
        value = float(self.set_process_value.text())
        self.file_sr_win.progressBar.setValue(value)
        if value >= 100:
            self.set_process_value.setText('0')
            print(self.set_process_value.text())

    def start_file_send_thread(self,local_path,filename,myID,aimID,file_win,send_sockfd,process_value):#启动发送文件线程
        content = 'put' + '*^$*#%*' + local_path + '*^$*#%*' + filename
        send_file = Thread(target=self.send_file,args=(content,myID,aimID,file_win,send_sockfd,process_value))
        send_file.setDaemon(True)
        send_file.start()

    def thread_show_file_sr(self):#子线程收到消息后从主线程打开文件收发窗口
        file_r_info = self.file_r_info
        self.show_file_sr(self.file_r_info[0],self.file_r_info[1],self.file_r_info[2],self.file_r_info[3],'recv')

    def agree_trans(self,friendID,myID,filename):#同意接收文件
        self.file_sr_win.RecvButton.hide()
        self.file_sr_win.StatusLabel.setText('接收中...')
        self.start_file_recv_thread(filename,friendID,myID,self.file_sr_win,self.set_process_value)

    def interrupt_trans(self,myID,filename):#拒绝接收文件或者中断文件传输
        self.file_sr_win.close()
        if self.file_is_sending:
            self.file_sr_win.interupt_flag.setText('True')
            msg = '0642 ' + filename
            self.send_sockfd.sendto(msg.encode(),self.server_addr)
        else:
            msg = '0642 ' + filename
            self.send_sockfd.sendto(msg.encode(),self.server_addr) 

    def recv_file(self,content,friendID,myID,file_win,process_value):#接收文件
        self.file_is_sending = True
        self.client.handle_normal_file(content,myID,file_win,process_value)
        self.file_is_sending = False
        #文件接收完毕，在消息文件中添加一条信息
        if file_win.interupt_flag.text() == 'False':
            print("文件接收完毕")
            filename = content.split('*^$*#%*')[1]
            localpath = 'Top files/%s/FileRecv/%s'%(myID,filename)
            message_record_path = 'Top files\\%s\\message_record.txt'%myID
            while True:
                try:
                    with open(message_record_path,'at') as f:
                        time_tamp = datetime.now()
                        msg = '038 ' + friendID + ' ' + myID + ' ' + localpath + ' ' + str(time_tamp) + '\n'
                        f.write(msg)
                        break
                except Exception:
                    continue
            file_win.close()
            if self.reshow_msgbox_signal.text() == '1':
                self.reshow_msgbox_signal.setText('2')
            else:
                self.reshow_msgbox_signal.setText('1')

    def start_file_recv_thread(self,filename,friendID,myID,file_win,process_value):#启动接收文件线程
        content = 'get' + '*^$*#%*' + filename
        send_file = Thread(target=self.recv_file,args=(content,friendID,myID,file_win,process_value))
        send_file.setDaemon(True)
        send_file.start()

    def recv_message(self):#收消息
        while True:
            data,addr = self.recv_sockfd.recvfrom(1024)
            self.isviewed = False
            message = data.decode().split(' ')
            print(message)
            if message[0] == "063":#处理接收到的普通消息
                time_tamp = str(datetime.now()).split(' ')
                message[-2:] = time_tamp
                temp = message[2].split("//*//#")
                message[2] = temp[0]
                message.insert(3,temp[1])
                path = 'Top files\\' + self.my_info[0] + '\\temp_conversation.txt'
                f = open(path,'rt')
                for i in f.readlines():
                    if i.rstrip() == message[1]:
                        break
                else:
                    f.close()
                    f = open(path,'at')
                    f.write(message[1]+'\n')
                    f.close()
                f.close()
                temp = ''
                for i in message:
                    temp += i
                    temp += ' '
                path = 'Top files\\' + self.my_info[0] + '\\temp_message.txt'
                with open(path,'at') as f:
                    f.write(temp.rstrip()+'\n')
                f.close()
                try:
                    if temp.split(' ')[1] == self.name_count[1]:
                        self.invert_message_status(self.name_count[1])
                        if self.reshow_msgbox_signal.text() == '1':
                            self.reshow_msgbox_signal.setText('2')
                        else:
                            self.reshow_msgbox_signal.setText('1')
                    if self.new_table.isVisible():
                        if self.reshow_temp_list_signal.text() == '1':
                            self.reshow_temp_list_signal.setText('2')
                        else:
                            self.reshow_temp_list_signal.setText('1')
                except AttributeError:
                    pass
                self.message_hint()

            elif message[0] == "065":#发送图片
                result_path = message[3] + ' ' + message[4]
                local_path = self.pic_waitting_tobesend[result_path]
                del self.pic_waitting_tobesend[result_path]
                myID = self.my_info[0]
                aimID = self.name_count[1]
                self.start_pic_send_thread(local_path,result_path,myID,aimID)

            elif message[0] == "0651":#接收图片
                filename = message[3]
                self.start_pic_recv_thread(filename,self.my_info[0])

            elif message[0] == "038":#处理接收文件传输请求
                print("收到一个文件接收请求")
                location = (self.geometry().x()+1050,self.geometry().y())
                file_size = int(message[4])
                path = 'Top files\\%s\\FileRecv\\%s'%(self.my_info[0],message[3])
                if os.path.exists(path):
                    index = 1
                    while True:
                        filename = message[3].split('.')[0]+'(%d)'%index + '.' + message[3].split('.')[1]
                        new_path = 'Top files\\%s\\FileRecv\\%s'%(self.my_info[0],filename)
                        if os.path.exists(new_path):
                            index +=1
                            continue
                        else:
                            f = open(new_path,'x')
                            f.close()
                            icon_path,filename = getIcon(new_path)
                            self.file_r_info = [location,icon_path,filename,file_size,message[1],message[2],message[3]]
                            if self.thread_show_file_sr_signal.text() == '1':
                                self.thread_show_file_sr_signal.setText('2')
                            else:
                                self.thread_show_file_sr_signal.setText('1')
                            break
                else:
                    filename = message[3]
                    new_path = 'Top files\\%s\\FileRecv\\%s'%(self.my_info[0],filename)
                    f = open(new_path,'x')
                    f.close()
                    icon_path,filename = getIcon(new_path)
                    self.file_r_info = [location,icon_path,filename,file_size,message[1],message[2],message[3]]
                    if self.thread_show_file_sr_signal.text() == '1':
                        self.thread_show_file_sr_signal.setText('2')
                    else:
                        self.thread_show_file_sr_signal.setText('1')

            elif message[0] == "066":#语音通话请求
                #启动语音聊天窗口
                self.thread_show_voice_chat_win.setText('%s %s %s'%(message[1],message[3],message[4]))

            elif message[0] == "0661":#对方接受语音请求
                self.aimuser_agree_achat.setText('%s %s'%(message[3],message[4]))
            
            elif message[0] == "0662":#收到中断语音聊天的信号
                self.interupt_achat.setText('%s %s %s'%(message[1],message[2],message[3]))

            elif message[0] == "067":#视频通话请求
                #启动视频聊天窗口
                self.thread_show_video_chat_win.setText('%s %s %s'%(message[1],message[3],message[4]))

            elif message[0] == "0671":#对方接受视频请求
                self.aimuser_agree_vchat.setText('%s %s'%(message[3],message[4]))

            elif message[0] == "0672":#收到中断视频的信号
                self.interupt_vchat.setText('%s %s %s'%(message[1],message[2],message[3]))

            elif message[0] == "031":#收到查询好友的回复
                print("查找到的好友：",message)
                self.recv_find_friends_rsp.setText(message[1])

            elif message[0] == "0310":#收到好友请求
                print("有人请求添加好友")
                self.friend_request_signal.setText("%s"%message[1])

            elif message[0] == "0311":#添加好友成功
                time.sleep(3)
                self.friends_info[message[1]] = ''
                if self.reshow_friends_list_signal2.text() == '2':
                    self.reshow_friends_list_signal2.setText('1')
                else:
                    self.reshow_friends_list_signal2.setText('2')


    def start_child_thread(self):#启动收消息线程
        recv_thread = Thread(target=self.recv_message)
        recv_thread.setDaemon(True)
        recv_thread.start()

    def reshow_msgbox(self):#重绘消息显示框
        print('重新显示函数触发')
        try:
            self.create_message_item(self.name_count[1])
        except AttributeError:
            pass

    def menu_show_close(self):#打开关闭菜单
        if self.menuisshow == False:
            self.pushButton_6.show()
            self.pushButton_5.show()
            self.menuisshow = True
        elif self.menuisshow == True:
            self.pushButton_5.close()
            self.pushButton_6.close()
            self.menuisshow = False
    
    def show_person_info(self):#打开个人信息窗口
        self.personal_win = PersonInfo(self.my_info)
        self.personal_win.show()
    
    def show_friend_info(self,myID,info_list):#显示好友信息Frame
        self.friend_info_frame = FriendFrame(myID,info_list,self)
        self.friend_info_frame.move(330,30)
        self.friend_info_frame.show()

    def create_message_item(self,friendID):#在聊天框中显示聊天信息
        self.tableWidget.clear()
        path = 'Top files\\' + self.my_info[0] + '\\message_record.txt'
        with open(path,'rt') as f:
            messages = []
            for i in f.readlines():
                temp = i.split(' ')
                if temp[1] == friendID or temp[2] == friendID:
                    messages.append(temp)
            rows = len(messages)
        f.close()
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.setStyleSheet('''QTableWidget::item:selected {background-color: rgb(250, 250, 250)}
                                        QTableWidget{border:0px;background-color:rgb(250,250,250);color:rgb(250,250,250)}''')
        #设置列宽
        self.tableWidget.setColumnWidth(0,9)
        self.tableWidget.setColumnWidth(1,60)
        self.tableWidget.setColumnWidth(2,560)
        self.tableWidget.setColumnWidth(3,60)
        self.tableWidget.setColumnWidth(4,9)
        self.tableWidget.verticalScrollBar().setStyleSheet('''
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
        '''
        )

        line = 0
        for i in messages:
            #绘制普通消息框
            if i[0] == '063' or i[0] == '036':
                if i[1] == friendID:
                    head_pic = QFrame()
                    head_pic.resize(60,50)
                    button = QPushButton(head_pic)
                    button.resize(45,45)
                    button.move(10,10)
                    icon = QtGui.QIcon(self.friends_info[i[1]][1])
                    button.setIcon(icon)
                    button.setIconSize(QtCore.QSize(45,45))
                    button.setCursor(Qt.PointingHandCursor)
                    self.tableWidget.setCellWidget(line,1,head_pic)

                    message = ''
                    for j in i[3:-2:1]:
                        message += j
                        message += ' '
                    msg_box = Friend_message(message.rstrip())
                    msg_box.text_label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    msg_box.text_label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.tableWidget.setCellWidget(line,2,msg_box)
                    msg_box.setGeometry(QtCore.QRect(0,0,400,27*1.5))
                    self.tableWidget.setRowHeight(line,msg_box.height+15)
                    time_box = QTableWidgetItem(i[-2]+' '+i[-1])
                    self.tableWidget.setItem(line,4,time_box)

                elif i[2] == friendID:
                    head_pic = QFrame()
                    head_pic.resize(60,50)
                    button = QPushButton(head_pic)
                    button.resize(45,45)
                    button.move(10,10)
                    icon = QtGui.QIcon(self.my_info[5])
                    button.setIcon(icon)
                    button.setIconSize(QtCore.QSize(45,45))
                    button.setCursor(Qt.PointingHandCursor)
                    self.tableWidget.setCellWidget(line,3,head_pic)

                    message = ''
                    for j in i[3:-2:1]:
                        message += j
                        message += ' '
                    msg_box = Mine_message(message.rstrip())
                    msg_box.text_label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    msg_box.text_label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    msg_box.text_label.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.tableWidget.setCellWidget(line,2,msg_box)
                    msg_box.setGeometry(QtCore.QRect(0,0,400,27*1.5))
                    self.tableWidget.setRowHeight(line,msg_box.height+15)

                    time_box = QTableWidgetItem(i[-2]+' '+i[-1])
                    self.tableWidget.setItem(line,4,time_box)
            #绘制文件消息框
            elif i[0] == '038':
                if i[1] == friendID:
                    head_pic = QFrame()
                    head_pic.resize(60,50)
                    button = QPushButton(head_pic)
                    button.resize(45,45)
                    button.move(10,10)
                    icon = QtGui.QIcon(self.friends_info[i[1]][1])
                    button.setIcon(icon)
                    button.setIconSize(QtCore.QSize(45,45))
                    button.setCursor(Qt.PointingHandCursor)
                    self.tableWidget.setCellWidget(line,1,head_pic)

                    message = ''
                    for j in i[3:-2:1]:
                        message += j
                        message += ' '
                    msg_box = Friend_file_message(message.rstrip())
                    self.tableWidget.setCellWidget(line,2,msg_box)
                    msg_box.setGeometry(QtCore.QRect(0,0,400,140))
                    self.tableWidget.setRowHeight(line,140)

                    time_box = QTableWidgetItem(i[-2]+' '+i[-1])
                    self.tableWidget.setItem(line,4,time_box)

                elif i[2] == friendID:
                    head_pic = QFrame()
                    head_pic.resize(60,50)
                    button = QPushButton(head_pic)
                    button.resize(45,45)
                    button.move(10,10)
                    icon = QtGui.QIcon(self.my_info[5])
                    button.setIcon(icon)
                    button.setIconSize(QtCore.QSize(45,45))
                    button.setCursor(Qt.PointingHandCursor)
                    self.tableWidget.setCellWidget(line,3,head_pic)

                    message = ''
                    for j in i[3:-2:1]:
                        message += j
                        message += ' '
                    msg_box = My_file_message(message.rstrip())
                    self.tableWidget.setCellWidget(line,2,msg_box)
                    msg_box.setGeometry(QtCore.QRect(150,10,400,140))
                    msg_box.open_file_button.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
                    msg_box.open_dir_button.setCursor(QtGui.QCursor(Qt.PointingHandCursor))
                    self.tableWidget.setRowHeight(line,140)

                    time_box = QTableWidgetItem(i[-2]+' '+i[-1])
                    self.tableWidget.setItem(line,4,time_box)
            line += 1
        self.tableWidget.sortItems(4,QtCore.Qt.AscendingOrder)
        self.tableWidget.scrollToBottom()

    def invert_message_status(self,friendID):#把未读消息转换成已读
        path1 = 'Top files\\' + self.my_info[0] + '\\temp_message.txt'
        path2 = 'Top files\\' + self.my_info[0] + '\\message_record.txt'
        f1 = open(path1,'r')
        f2 = open(path2,'a')
        messages_lift = []
        for i in f1.readlines():
            if i.split(' ')[1] == friendID:
                f2.write(i)
                continue
            else:
                messages_lift.append(i)
        f1.close()
        f2.close()
        f3 = open(path1,'w')
        f3.writelines(messages_lift)
        f3.close()

    def message_hint(self):#显示未读消息数量
        path = 'Top files\\%s\\temp_message.txt'%self.my_info[0]
        with open(path,'rt') as f:
            count = len(f.readlines())
        self.label_3.setText(str(count))
        if int(self.label_3.text()) < 10:
            self.label_3.resize(20,20)
        elif int(self.label_3.text()) <100:
            self.label_3.resize(25,20)
        else:
            self.label_3.resize(32,20)
        self.label_3.show()
        if self.label_3.text() == '0':
            self.label_3.hide()

    def open_expression(self):#打开表情窗口
        self.expression_form = ExpressionForm(self)
        self.expression_form.show()
        self.expression_form.tableWidget.itemClicked.connect(self.handle_expression_click) #响应表情点击的Item事件

    def handle_expression_click(self,item):#表情点击响应函数
        self.textEdit.insertHtml("<img src='expression/fun/10%d%d.png'>"%(item.row(),item.column()))
        self.expression_form.hide()
        self.textEdit.setFocus()

    #语音聊天
    def voice_chat(self,mode,send_sockfd=None,my_id=None,friend_id=None,c_server_addr=None,server_addr=None,reshow_signal=None):#语音聊天
        location = (self.geometry().x()+1050,self.geometry().y())
        if mode == "request":
            #打开语音聊天窗口
            self.voice_chat_win = VoiceChatWin(location,mode,send_sockfd,my_id,friend_id,c_server_addr,server_addr,reshow_signal)
            self.voice_chat_win.show()
            #发起语音请求
            hostname = gethostname()
            ip = gethostbyname(hostname)
            msg = '066 ' + self.my_info[0] + ' ' + self.name_count[1] + ' ' + ip + ' ' + '10088'
            self.send_sockfd.sendto(msg.encode(),self.server_addr)
            #开启音频流接收服务
            self.voice_chat_win.req_voice_server = AudioServer(10088,4)
        else:
            self.voice_chat_win = VoiceChatWin(location,mode,send_sockfd,my_id,friend_id,c_server_addr,server_addr,reshow_signal)
            self.voice_chat_win.show()
            nick_name = self.friends_info[friend_id][0]
            self.voice_chat_win.label_3.setText(nick_name)

    def response_voice(self):#接收方显示语音聊天窗口
        if self.thread_show_voice_chat_win.text() == 'Null':
            return
        data = self.thread_show_voice_chat_win.text()
        self.thread_show_voice_chat_win.setText('Null')
        friend_id = data.split(' ')[0]
        ip = data.split(' ')[1]
        port = int(data.split(' ')[2])
        c_server_addr = (ip,port)
        self.voice_chat('response',self.send_sockfd,self.my_info[0],friend_id,c_server_addr,self.server_addr,self.reshow_msgbox_signal)

    def handle_aimagree_achat(self):#发起方收到同意语音信号,开始语音聊天
        if self.aimuser_agree_achat.text() == 'Null':
            return
        ip = self.aimuser_agree_achat.text().split(' ')[0]
        port = int(self.aimuser_agree_achat.text().split(' ')[1])
        self.aimuser_agree_achat.setText('Null')
        self.voice_chat_win.audio_chat_staus = True
        self.voice_chat_win.req_voice_client = AudioClient(ip,port,4)
        #设置按钮可点击
        self.voice_chat_win.Micro.setEnabled(True)
        self.voice_chat_win.Volume.setEnabled(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/05-08.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.voice_chat_win.Volume.setIcon(icon)
        self.voice_chat_win.Volume.setIconSize(QtCore.QSize(32, 32))
        #开启新线程计时
        th = Thread(target=self.count_time,args=(self.voice_chat_win.label_3,))
        th.setDaemon(True)
        th.start()

    def handle_achat_interupt(self):#收到终止语音聊天的信号
        if self.interupt_achat.text() == 'Null':
            return
        message = self.interupt_achat.text().split(' ')
        self.interupt_achat.setText('Null')
        mode = message[2]
        if mode == 'request':#发起方发来的信号
            time_tamp = str(datetime.now())
            msg = '063 ' + message[0] + ' ' + message[1] + ' ' + '语音通话: %s'%self.voice_chat_win.label_3.text() + ' ' + time_tamp + '\n'
            path = 'Top files\\%s\\message_record.txt'%self.my_info[0]
            try:
                with open(path,'a') as f:
                    f.write(msg)
                f.close()
            except:
                pass
            if self.reshow_msgbox_signal.text() == '1':
                self.reshow_msgbox_signal.setText('2')
            else:
                self.reshow_msgbox_signal.setText('1')
            self.voice_chat_win.label_3.setText('Null')
            try:
                print("关闭接收方音频服务")
                del self.voice_chat_win.rsp_voice_server
            except:
                pass
            try:
                print("关闭接收方音频客户端")
                del self.voice_chat_win.rsp_voice_client
            except:
                pass
            self.voice_chat_win.close()
        else:
            time_tamp = str(datetime.now())
            msg = '036 ' + message[1] + ' ' + message[0] + ' ' + '语音通话: %s'%self.voice_chat_win.label_3.text() + ' ' + time_tamp + '\n'
            path = 'Top files\\%s\\message_record.txt'%self.my_info[0]
            try:
                with open(path,'a') as f:
                    f.write(msg)
                f.close()
            except:
                pass
            if self.reshow_msgbox_signal.text() == '1':
                self.reshow_msgbox_signal.setText('2')
            else:
                self.reshow_msgbox_signal.setText('1')
            self.voice_chat_win.label_3.setText('Null')
            try:
                print("关闭请求方音频服务")
                del self.voice_chat_win.req_voice_server
            except:
                pass
            try:
                print("关闭请求方音频客户端")
                del self.voice_chat_win.req_voice_client
            except:
                pass
            self.voice_chat_win.close()

    #视频聊天
    def video_chat(self,mode,send_sockfd=None,friend_id=None,c_server_addr=None,server_addr=None,reshow_signal=None):#视频聊天
        location = (self.geometry().x()+1050,self.geometry().y())
        if mode == "request":
            #打开视频聊天窗口
            my_id = self.my_info[0]
            self.video_chat_win = VideoChatWin(location,mode,send_sockfd,my_id,friend_id,c_server_addr,server_addr,reshow_signal)
            self.video_chat_win.show()
            path = self.friends_info[self.name_count[1]][1]
            self.video_chat_win.HeadPic.setPixmap(QtGui.QPixmap(path))
            #发起视频请求
            hostname = gethostname()
            ip = gethostbyname(hostname)
            msg = '067 ' + self.my_info[0] + ' ' + self.name_count[1] + ' ' + ip + ' ' + '10086'
            self.send_sockfd.sendto(msg.encode(),self.server_addr)
            #开启视频流和音频流接收服务
            self.video_chat_win.req_video_server = VideoServer(10086,self.video_chat_win.FriendVideoLabel)
        else:
            my_id = self.my_info[0]
            self.video_chat_win = VideoChatWin(location,mode,send_sockfd,my_id,friend_id,c_server_addr,server_addr,reshow_signal)
            self.video_chat_win.show()
            #显示请求视频的好友头像
            path = self.friends_info[friend_id][1]
            self.video_chat_win.HeadPic.setPixmap(QtGui.QPixmap(path))
            #显示请求视频的好友昵称
            nick_name = self.friends_info[friend_id][0]
            self.video_chat_win.label.setText(nick_name)

    def response_video(self):#接收方显示视频聊天窗口
        if self.thread_show_video_chat_win.text() == 'Null':
            return
        data = self.thread_show_video_chat_win.text()
        self.thread_show_video_chat_win.setText('Null')
        friend_id = data.split(' ')[0]
        ip = data.split(' ')[1]
        port = int(data.split(' ')[2])
        c_server_addr = (ip,port)
        self.video_chat('response',self.send_sockfd,friend_id,c_server_addr,self.server_addr,self.reshow_msgbox_signal)

    def handle_aimagree_vchat(self):#发起方收到同意视频信号,开始视频聊天
        if self.aimuser_agree_vchat.text() == 'Null':
            return
        self.video_chat_win.cap.release()
        self.video_chat_win.HeadPic.hide()
        ip = self.aimuser_agree_vchat.text().split(' ')[0]
        port = int(self.aimuser_agree_vchat.text().split(' ')[1])
        self.aimuser_agree_vchat.setText('Null')
        self.video_chat_win.video_chat_staus = True
        self.video_chat_win.req_video_client = VideoClient(ip,port,self.video_chat_win.MyVideoLabel)
        #设置按钮可点击
        self.video_chat_win.Mute.setEnabled(True)
        self.video_chat_win.Switch.setEnabled(True)
        self.video_chat_win.Volume.setEnabled(True)
        #开启新线程计时
        th = Thread(target=self.count_time,args=(self.video_chat_win.label,))
        th.setDaemon(True)
        th.start()

    def handle_vchat_interupt(self):#收到终止视频聊天的信号
        if self.interupt_vchat.text() == 'Null':
            return
        message = self.interupt_vchat.text().split(' ')
        self.interupt_vchat.setText('Null')
        mode = message[2]
        if mode == 'request':#发起方发来的信号
            time_tamp = str(datetime.now())
            msg = '063 ' + message[0] + ' ' + message[1] + ' ' + '视频通话: %s'%self.video_chat_win.label.text() + ' ' + time_tamp + '\n'
            path = 'Top files\\%s\\message_record.txt'%self.my_info[0]
            try:
                with open(path,'a') as f:
                    f.write(msg)
                f.close()
            except:
                pass
            if self.reshow_msgbox_signal.text() == '1':
                self.reshow_msgbox_signal.setText('2')
            else:
                self.reshow_msgbox_signal.setText('1')
            self.video_chat_win.label.setText('Null')
            try:
                del self.video_chat_win.rsp_video_server
                print("关闭接收方的视频服务")
            except:
                pass
            try:
                del self.video_chat_win.rsp_video_client
                print("关闭接收方的视频客户端")
            except:
                pass
            self.video_chat_win.close()
        else:
            time_tamp = str(datetime.now())
            msg = '036 ' + message[1] + ' ' + message[0] + ' ' + '视频通话: %s'%self.video_chat_win.label.text() + ' ' + time_tamp + '\n'
            path = 'Top files\\%s\\message_record.txt'%self.my_info[0]
            try:
                with open(path,'a') as f:
                    f.write(msg)
                f.close()
            except:
                pass
            if self.reshow_msgbox_signal.text() == '1':
                self.reshow_msgbox_signal.setText('2')
            else:
                self.reshow_msgbox_signal.setText('1')
            self.video_chat_win.label.setText('Null')
            try:
                del self.video_chat_win.req_video_server
                print("关闭请求方的视频服务")
            except:
                pass
            try:
                del self.video_chat_win.req_video_client
                print("关闭请求方的视频客户端")
            except:
                pass
            self.video_chat_win.close()

    def count_time(self,label):#计时函数
        s1 = 0
        s2 = 0
        m1 = 0
        m2 = 0
        while True:
            if label.text() == 'Null':
                print("计时终止")
                break
            if s1 == 10:
                s1 = 0
                s2 += 1
            if s2 == 6:
                s2 = 0
                m1 += 1
            if m1 == 10:
                m1 = 0
                m2 += 1
            count = str(m2)+str(m1)+':'+str(s2)+str(s1)
            label.setText(count)
            time.sleep(1)
            s1 += 1    

    #添加好友、加群
    def open_add_win(self):#打开添加窗口
        self.add_win = AddWin(self.send_sockfd,self.server_addr,self.my_info[0])
        self.add_win.show()

    def start_recv_friends_info(self,friends_id,addwin):#启动接收查询到的用户信息的线程
        if self.recv_find_friends_rsp.text() == 'Null':
            return
        self.recv_find_friends_rsp.setText('Null')
        if friends_id == 'False':
            addwin.label_7.setText("查找失败...")
            addwin.label_7.show()
            addwin.label_3.hide()
            addwin.scrollArea.close()
            try:
                for i in self.add_win.item_list:
                    i.close()
                    self.add_win.item_list.remove(i)
                    del i
                    print(self.add_win.item_list)
            except:
                pass
        else:
            addwin.label_7.setText("正在加载...")
            addwin.label_7.show()
            addwin.scrollArea.show()
            th = Thread(target=self.recv_friends_info,args=(friends_id,addwin))
            th.setDaemon(True)
            th.start()

    def recv_friends_info(self,friends_id,addWin):#接收用户信息
        tcp_sockfd = socket()
        tcp_server_addr = ('176.209.106.8', 6970)
        # tcp_server_addr = ('192.168.199.195',6970)
        tcp_sockfd.connect(tcp_server_addr)
        ids = friends_id.split('#')
        tcp_sockfd.send(friends_id.encode())
        fmt = 'i'
        st = Struct(fmt)
        self.friends_item_info = {}
        for i in ids:
            personal_info = []
            while True:
                Header = tcp_sockfd.recv(4)
                length = st.unpack(Header)[0]
                data = tcp_sockfd.recv(length)
                while len(data) < length:
                    data += tcp_sockfd.recv(length-len(data))
                personal_info.append(data)
                print(len(data))
                try:
                    division = data.decode()
                except Exception:
                    division = ''
                if division == '##':
                    self.friends_item_info[personal_info[0]]=[personal_info[1],personal_info[2],personal_info[3],personal_info[4]]
                    print("成功接收好友消息")
                    break
                elif division == '***':
                    self.friends_item_info[personal_info[0]]=[personal_info[1],personal_info[2],personal_info[3],personal_info[4]]
                    print("好友消息接收完毕")
                    break
        addWin.label_7.setText('')
        if self.show_friend_item.text == '2':
            self.show_friend_item.setText('1')
        else:
            self.show_friend_item.setText('2')

    def show_friends_item(self):#显示好友Item
        if self.show_friend_item.text() == 'Null':
            return
        self.show_friend_item.setText('Null')
        self.add_win.label_3.show()
        index = 1
        try:
            for i in self.add_win.item_list:
                i.close()
                self.add_win.item_list.remove(i)
                del i
                print(self.add_win.item_list)
        except:
            pass
        self.add_win.item_list = []
        index = 1
        f_line_location = [50,5]
        s_line_location = [50,105]
        for i in self.friends_item_info:
            my_id = self.my_info[0]
            aim_id = i.decode()
            nick_name = self.friends_item_info[i][0].decode()
            birth = self.friends_item_info[i][1].decode()
            birth_year = int(birth[0:4])
            print(birth_year)
            age = str(date.today().year - birth_year)
            gender_code = self.friends_item_info[i][2].decode()
            if gender_code == '0':
                gender = '男'
            elif gender_code == '1':
                gender = '女'
            else:
                gender = "未知"
            pic_bytes = self.friends_item_info[i][3]
            self.add_win.scrollArea.item = Friend_info_item(self.friends_info,my_id,aim_id,nick_name,age,gender,pic_bytes,self.send_sockfd,self.server_addr,self.add_win.scrollArea)
            self.add_win.item_list.append(self.add_win.scrollArea.item)
            self.add_win.scrollArea.item.show()
            if index % 2 == 1:
                f_line_location[0] += 50
                self.add_win.scrollArea.item.move(f_line_location[0],f_line_location[1])
            else:
                s_line_location[0] += 50
                self.add_win.scrollArea.item.move(s_line_location[0],s_line_location[1])
            index += 1
        print("好友消息接收完毕")

    def handle_friend_request(self):#处理添加好友请求
        if self.friend_request_signal.text == 'Null':
            return
        friend_id = self.friend_request_signal.text()
        self.friend_request_signal.setText('Null')
        self.dialog = FrirenRequestWin(self.my_info[0],friend_id,self.friends_info,self.reshow_friends_list_siganl,self.send_sockfd,self.server_addr)
        self.dialog.show()

    def recv_show_friends_list(self):#接收好友列表
        friends_id = ''
        for i in self.friends_info:
            friends_id += (i+'#')
        friends_id = friends_id.rstrip('#')
        th = Thread(target=self.recv_info,args=(friends_id,))
        th.setDaemon(True)
        th.start()

    def recv_info(self,friends_id):
        tcp_sockfd = socket()
        tcp_server_addr = ('176.209.106.8', 6970)
        # tcp_server_addr = ('192.168.199.195',6970)
        tcp_sockfd.connect(tcp_server_addr)
        ids = friends_id.split('#')
        tcp_sockfd.send(friends_id.encode())
        fmt = 'i'
        st = Struct(fmt)
        self.friends_info = {}
        for i in ids:
            personal_info = []
            while True:
                Header = tcp_sockfd.recv(4)
                length = st.unpack(Header)[0]
                data = tcp_sockfd.recv(length)
                while len(data) < length:
                    data += tcp_sockfd.recv(length-len(data))
                personal_info.append(data)
                print(len(data))
                try:
                    division = data.decode()
                except Exception:
                    division = ''
                if division == '##':
                    f = open('temp_info/'+personal_info[0].decode()+'.jpg','wb')
                    f.write(personal_info[4])
                    f.close()
                    self.friends_info[personal_info[0].decode()]=[personal_info[1].decode(),'temp_info/'+personal_info[0].decode()+'.jpg']
                    print("成功接收好友消息")
                    break
                elif division == '***':
                    f = open('temp_info/'+personal_info[0].decode()+'.jpg','wb')
                    f.write(personal_info[4])
                    f.close()
                    self.friends_info[personal_info[0].decode()]=[personal_info[1].decode(),'temp_info/'+personal_info[0].decode()+'.jpg']
                    print("好友消息接收完毕")
                    break
        print(self.friends_info)
        

