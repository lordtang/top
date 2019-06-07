from socket import *
from threading import Thread
from struct import Struct
from datetime import datetime
import time
import hashlib

import sys,os
 

class PrivateChatRoomClient():
    def __init__(self):
        self.addr = ('0.0.0.0',8080)
        self.server_addr = ('176.209.106.8', 8080)
        self.server_file_addr = ('176.209.106.8', 6969)
        # self.server_addr = ('192.168.199.195', 8080)
        # self.server_file_addr = ('192.168.199.195', 6969)

    def open_client(self):#一级目录包括登录、注册、忘记密码和退出操作
        #一级目录里的操作使用tcp连接
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        try:
            self.sockfd.connect(self.server_addr)
            print("连接服务器成功")
        except OSError:
            pass
    
    def do_login(self, sockfd,count, password):#登录操作 账号和密码都不能有空格，也不能为空
        msg = '011' + ' ' + count + ' ' + password
        self.count = count
        try:
            sockfd.send(msg.encode())
            data = sockfd.recv(1024)           #超时检测，还未写
            print(data.decode().split()[1])
            config = data.decode().split()[1]
            #发送登录请求后，如果登录成功会收到'011 OK',如果失败会收到'011 Failed'
            if config == 'OK':
                # sockfd.close()    #登录成功，断开Tcp连接
                return True
            else:
                return False
        except OSError:
            return False

    def log_success_recv(self, sockfd):#登录成功开始接收个人和好友信息、离线消息
        fmt = 'i'
        st = Struct(fmt)
        myinfo = []
        friends_info = {}
        while True:
            Header = sockfd.recv(4)
            length = st.unpack(Header)[0]
            data = sockfd.recv(length)
            if len(data) < length:
                data += sockfd.recv(length-len(data))
            try:
                division = data.decode()
                print(division)
            except Exception:
                division = ''
            if division == '###':
                receive_finished = False
                new_user = False
                while True:
                    personal_info = []
                    while True:
                        Header = sockfd.recv(4)
                        length = st.unpack(Header)[0]
                        data = sockfd.recv(length)
                        if len(data) < length:
                            data += sockfd.recv(length-len(data))
                        try:
                            if data.decode() == 'new':
                                new_user = True
                                break
                        except Exception:
                            pass
                        personal_info.append(data)
                        try:
                            division = data.decode()
                        except Exception:
                            division = ''
                        if division == '##':
                            friends_info[personal_info[0]]=[personal_info[1],personal_info[2]]
                            print("成功接收好友消息")
                            break
                        elif division == '***':
                            friends_info[personal_info[0]]=[personal_info[1],personal_info[2]]
                            print("好友消息接收完毕")
                            receive_finished = True
                            break
                    if receive_finished:
                        break
                    if new_user:
                        break     
                break
            
            myinfo.append(data)
        return myinfo,friends_info

    def request(self, sockfd, username):#注册查询用户名是否重复
        msg = "0121" + ' ' + username
        try:
            sockfd.send(msg.encode())
            data = sockfd.recv(1024).decode()
            config = data.split(' ')[1]
            print(config)
            if config == "OK":
                return True
            else:
                return False
        except Exception:
            pass
            print("消息未发送")

    def register(self,username,password,gender,birth,tel):#注册包括昵称、密码、性别、出生日期和电话号码。性别为选填
        msg = '012' + ' ' + username + ' ' + password + ' ' + gender + ' ' + birth + ' ' + tel
        try:
            self.sockfd.send(msg.encode())
        except Exception:
            return False
        else:
            data = self.sockfd.recv(1024).decode().split(' ')
            config = data[1]
            count = data[2]
            if  config:
                return (True,count)
            else:
                return (False,count)

    def forget_pw_request(self, sockfd, count):#找回密码查询是否有这个账号
        msg = "0131" + ' ' + count
        try:
            sockfd.send(msg.encode())
            data = sockfd.recv(1024).decode().split(' ')
            print(data)
            return data
        except Exception:
            return ['0131','ConnectFailed','N']

    def forget_pw(self, sockfd, count, newpassword):#忘记密码，找回密码
        msg = '013 ' + count + ' ' + newpassword
        sockfd.send(msg.encode())
        data = sockfd.recv(1024).decode().split(' ')
        config = data[1]
        if config == 'OK':
            return True
        else:
            return False

    def send_message(self,udp_socket,myID,aimID,text):#发送普通文本消息
        try:
            time_stamp = datetime.now()
            time_stamp = str(time_stamp)
            msg = '036'+ ' ' + myID + ' ' + aimID + ' ' + text + ' ' + time_stamp
            print("msg:",msg)
            udp_socket.sendto(msg.encode(),self.server_addr)
        except Exception:
            print("发送失败")
    
    def send_pic_request(self,udp_sockfd,myID,aimID,pic_path):#用udp发送一个发送图片请求
        msg = '065 ' + myID + ' ' + aimID + ' ' + pic_path
        udp_sockfd.sendto(msg.encode(),self.server_addr)

    def send_file_request(self,udp_sockfd,myID,aimID,file_name,file_size):#用udp发送一个发送文件请求
        msg = '038 ' + myID + ' ' + aimID + ' ' + file_name + ' ' + str(file_size)
        udp_sockfd.sendto(msg.encode(),self.server_addr)
        print("向服务器发送了一条文件请求")

    def handle_file(self,content,myID):#处理图片的上传和接收
        '''
            图片处理函数
            content格式
            上传文件：put 'local_path' 'result_path'
            下载文件：get 'result_path'
        '''
        print("开始运行文件处理函数")
        client = socket()  # 生成socket连接对象
        client.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        ip_port = self.server_file_addr  # 服务器文件TCP套接字地址和端口号
        client.connect(ip_port)  # 连接
        print("传输服务连接成功")
        content = content
        if len(content)==0: 
            print("blocked")
        #客户端接收服务器文件
        print(content)
        if content.startswith("get"):
            file_name = content.split('*^$*#%*')[1]
            file_info = 'get'+ '*^$*#%*' + file_name +'*^$*#%*'+ '0'
            client.send(file_info.encode("utf-8"))  # 传送和接收都是bytes类 型
            # 1.先接收文件长度，建议8192
            server_response = client.recv(1024)
            if server_response.decode('utf-8').split(' ')[0] == 'F':
                #sys.exit('not found')
                pass
            else:
                file_size = int(server_response.decode("utf-8"))
                print("接收到的大小：", file_size)
                # 2.接收文件内容
                client.send("准备好接收".encode("utf-8"))  # 接收确认
                file_name = content.split("*^$*#%*")[1]
                path = "Top files\\%s\\image\\C2C\\%s"%(myID,file_name)
                f = open(path, "wb")
                received_size = 0
                m = hashlib.md5()
                while received_size < file_size:
                    size = 0  # 准确接收数据大小，解决粘包
                    if file_size - received_size > 1024: # 多次接收
                        size = 1024
                    else:  # 最后一次接收完毕
                        size = file_size - received_size
                    data = client.recv(size)  # 多次接收内容，接收大数据
                    data_len = len(data)
                    received_size += data_len
                    print("已接收：", int(received_size/file_size*100),"%")
                    m.update(data)
                    f.write(data)
                f.close()
                print("实际接收的大小:", received_size)  # 解码

                # 3.md5值校验
                md5_sever = client.recv(1024).decode("utf-8")
                md5_client = m.hexdigest()
                print("服务器发来的md5:", md5_sever)
                print("接收文件的md5:", md5_client)
                if md5_sever == md5_client:
                    print("MD5值校验成功")
                    # print('获取成功')
                    #sys.exit('获取成功')
                else:
                    print("MD5值校验失败")
        # 客户端向服务器发送文件
        elif content.startswith("put"):
            # local_path = ''
            local_path = content.split('*^$*#%*')[1]
                # local_path += i
            result_path = content.split('*^$*#%*')[2]
            file_name = result_path.split('\\')[-1]
            if os.path.isfile(local_path):  # 判断文件存在
                # 1.先发送文件大小，让服务端准备接收
                size = os.stat(local_path).st_size  #获取文件大小
                file_info = 'put' +'*^$*#%*'+ file_name +'*^$*#%*'+str(size)
                client.send(file_info.encode("utf-8"))
                # 2.发送文件内容
                client.recv(1024)  # 接收确认
                m = hashlib.md5()
                f = open(local_path, "rb")
                for line in f:
                    client.send(line)  # 发送数据
                    m.update(line)
                f.close()
                print("文件传输完成")
                # 3.发送md5值进行校验
                md5 = m.hexdigest()
                client.send(md5.encode("utf-8"))  # 发送md5值
                print("md5:", md5)
                data = client.recv(2048).decode()
                print("md5校验:",data)
                #sys.exit()
                # os._exit(1)
            #文件不存在
            else:
                #sys.exit('文件不存在，请重新输入')
                print("文件不存在")
                pass
        else:
            print('''
            for example>>get test.txt
                    >>put text.txt
            ''')
            #sys.exit()
        client.close()
        print("文件传输结束")

    def handle_normal_file(self,content,myID,file_win,process_value):#处理文件的上传和接收
        '''
            文件处理函数
            content格式
            上传文件：put 'filename' 'filepath'
            下载文件：get 'filename'
        '''
        print("开始运行文件处理函数")
        client = socket()  # 生成socket连接对象
        client.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        ip_port = self.server_file_addr  # 服务器文件TCP套接字地址和端口号
        client.connect(ip_port)  # 连接
        print("传输服务连接成功")
        content = content
        if len(content)==0: 
            print("blocked")
        #客户端接收服务器文件
        print(content)
        if content.startswith("get"):
            file_name = content.split('*^$*#%*')[1]
            file_info = 'get'+ '*^$*#%*' + file_name +'*^$*#%*'+ '0'
            client.send(file_info.encode("utf-8"))  # 传送和接收都是bytes类 型
            # 1.先接收文件长度，建议8192
            server_response = client.recv(1024)
            if server_response.decode('utf-8').split(' ')[0] == 'F':
                #sys.exit('not found')
                pass
            else:
                file_size = int(server_response.decode("utf-8"))
                print("接收到的大小：", file_size)
                # 2.接收文件内容
                client.send("准备好接收".encode("utf-8"))  # 接收确认
                file_name = content.split("*^$*#%*")[1]
                path = "Top files\\%s\\FileRecv\\%s"%(myID,file_name)
                f = open(path, "wb")
                received_size = 0
                m = hashlib.md5()
                while received_size < file_size:
                    size = 0  # 准确接收数据大小，解决粘包
                    if file_size - received_size > 1024: # 多次接收
                        size = 1024
                    else:  # 最后一次接收完毕
                        size = file_size - received_size
                    data = client.recv(size)  # 多次接收内容，接收大数据
                    data_len = len(data)
                    received_size += data_len
                    value = (received_size/file_size)*100
                    if file_win.interupt_flag.text() == 'True':
                        print("终止接收文件...")
                        client.close()
                        return
                    process_value.setText(str(value))
                    m.update(data)
                    f.write(data)
                f.close()
                print("实际接收的大小:", received_size)  # 解码

                # 3.md5值校验
                md5_sever = client.recv(1024).decode("utf-8")
                md5_client = m.hexdigest()
                print("服务器发来的md5:", md5_sever)
                print("接收文件的md5:", md5_client)
                if md5_sever == md5_client:
                    print("MD5值校验成功")
                    # print('获取成功')
                    #sys.exit('获取成功')
                else:
                    print("MD5值校验失败")
        # 客户端向服务器发送文件
        elif content.startswith("put"):
            file_win.StatusLabel.setText('文件上传中...')
            local_path = content.split('*^$*#%*')[1]
            file_name = content.split('*^$*#%*')[2]
            if os.path.isfile(local_path):  # 判断文件存在
                # 1.先发送文件大小，让服务端准备接收
                print("文件存在，开始准备发送")
                size = os.stat(local_path).st_size  #获取文件大小
                file_info = 'put' +'*^$*#%*'+ file_name +'*^$*#%*'+str(size)
                client.send(file_info.encode("utf-8"))
                # 2.发送文件内容
                client.recv(1024)  # 接收确认
                m = hashlib.md5()
                data_send = 0
                f = open(local_path, "rb")
                for line in f:
                    if file_win.interupt_flag.text() == 'True':
                        print("文件传输被终止...")
                        client.close()
                        return
                    client.send(line)  # 发送数据
                    m.update(line)
                    data_send += len(line)
                    value = (data_send/size)*100
                    process_value.setText(str(value))
                f.close()
                print("文件传输完成...")
                # file_win.close()
                # 3.发送md5值进行校验
                md5 = m.hexdigest()
                client.send(md5.encode("utf-8"))  # 发送md5值
                print("md5:", md5)
                data = client.recv(2048).decode()
                print("md5校验:",data)
                #sys.exit()
                # os._exit(1)
            #文件不存在
            else:
                #sys.exit('文件不存在，请重新输入')
                print("文件不存在")
                pass

        else:
            print('''
            for example>>get test.txt
                    >>put text.txt
            ''')
            #sys.exit()
        client.close()

