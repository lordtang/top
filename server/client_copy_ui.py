from socket import *
from threading import Thread
import sys,os
import time 

class PrivateChatRoomClient():
    
    def __init__(self):
        self.addr = ('176.209.108.62',8080)
        self.addr2 = ('176.209.108.62',8081)
        self.Thread_list = []
        self.function_list = []
        self.username = 'a'


    def step_1(self):#一级目录包括登录、注册、忘记密码和退出操作
        #一级目录里的操作使用tcp连接
        sockfd = socket()
        sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        sockfd.bind(self.addr)
        print("------1) 登录--------")
        print("------2) 注册--------")
        print("------3) 忘记密码-----")
        print("------4) 退出--------")
        op = input("input operation: ")
        if op == '1':
            self.do_login(sockfd)
        elif op == '2':
            self.register(sockfd)
        elif op == '3':
            self.forgetpw(sockfd)
        else:
            self.do_quit(sockfd)
    
    def step_2(self):#登录后的第二级，包括菜单，通讯录，群聊
        print("------1) 菜单--------")
        print("------2) 通讯录--------")
        print("------3) 群聊-----")
        op = input("input operation: ")
        if op == '1':
            self.step_3_menu()
        elif op == '2':
            self.chatting()
        elif op == '3':
            self.groupchat()

    #群聊里面有添加群成员，发送群信息，发送群文件，发送群图片
    def groupchat(self):
        print("----------1)添加群成员-------------")
        print("----------2)发送信息---------------")
        print("----------3)发送文件---------------")
        print("----------4)发送图片---------------")
        sockfd = socket(AF_INET,SOCK_DGRAM)
        op = input(">>> ")
        groupID = input("输入群ID: ")
        if op == '1':
            self.invite(groupID,sockfd)
        elif op == '2':
            self.groupmessage(groupID,sockfd)
        elif op == '3':
            self.groupfile(groupID,sockfd)
        elif op == '4':
            self.grouppic(groupID,sockfd)

    #邀请新的群成员
    def invite(self,groupID,sockfd):
        aimID = input("输入要添加的用户ID: ")
        msg = '051 ' + self.username + ' ' + groupID + ' ' + aimID
        sockfd.sendto(msg.encode(),self.addr)    
        sockfd.close()
        self.groupchat()

    #发送群信息
    def groupmessage(self,groupID,sockfd):
        while True:
            try:
                data = input("输入要发送的文字内容: ")
                msg = '052 '+self.username + ' ' + groupID + ' ' + data + '#seq=x'
                sockfd.sendto(msg.encode(),self.adddr)
            except KeyboardInterrupt as err:
                sockfd.close()
                self.groupchat()
    
    #发送群文件
    def groupfile(self,groupID,sockfd):
        msg = '053 ' + self.username + ' ' + groupID + 'file_name'
        sockfd.sendto(msg.encode(),self.addr)
        self.groupchat()

    #发送图片
    def grouppic(self,groupID,sockfd):
        msg = '054 ' + self.username + ' ' + groupID + 'pic_name'        
        sockfd.sendto(msg.encode(),self.addr)
        self.groupchat()

    def step_3_menu(self):#菜单的三级，包括个人信息，添加好友，发起群聊，添加群聊，设置，退出
        print("------1) 修改个人信息--------")
        print("------2) 添加好友--------")
        print("------3) 发起群聊-----")
        print("------4) 添加群聊--------")
        print("------5) 设置--------")
        print("------6) 退出-----")
        op = input("input operation: ")
        if op == '1':
            self.modify()
        elif op == '2':
            self.addfriend()
        elif op == '3':
            self.startgroupchat()
        elif op == '4':
            self.addgroupchat()
        elif op == '5':
            self.setting()
        elif op == '6':
            self.menu_quit()
            #do_quit
    
    #这是通讯录，里面有发送消息，发送图片，发送文件，发送文件和图片会用tcp发送
    def chatting(self):
        print("-----------1)发送信息---------------")
        print("-----------2)发送图片---------------")
        print("-----------3)发送文件---------------")
        print("-----------4) 退 出---------------")
        op = input(">>> ")
        if op == '1':
            self.send_message()
        elif op == '2':
            self.send_pic()
        elif op == '3':
            self.send_file()

    #发送文本信息，方便测试，循环发送，ctrl+c关闭udp套接字回到chatting()
    def send_message(self):
        sockfd = socket(AF_INET,SOCK_DGRAM)
        aimID = input("输入要发送的对象: ")
        while True:
            try:
                data = input("输入要发送的文字内容: ")
                msg = '036 '+self.username + ' ' + aimID + ' ' + data + '#seq=x'
                sockfd.sendto(msg.encode(),self.adddr)
            except KeyboardInterrupt as err:
                sockfd.close()
                self.chatting()

    #用udp发送一个发送图片请求，发送了就关闭udp套接字
    def send_pic(self):
        sockfd = socket(AF_INET,SOCK_DGRAM)
        aimID = input("输入要发送的对象: ")
        msg = '037 ' + self.username + ' ' + aimID + ' ' + 'pic_name'
        sockfd.sendto(msg.encode(),self.addr)
        sockfd.close()

    #用udp发送一个发送文件请求，发送了就关闭udp套接字
    def send_file(self):
        sockfd = socket(AF_INET,SOCK_DGRAM)
        aimID = input("输入要发送的对象: ")
        msg = '038 ' + self.username + ' ' + aimID + ' ' + 'file_name'
        sockfd.sendto(msg.encode(),self.addr)
        sockfd.close()
                
    def setting(self):
        pass#还不知道里面有什么

    #添加群聊
    def addgroupchat(self):
        sockfd = socket(AF_INET,SOCK_DGRAM)
        print("-----|查找群|: |输入群ID|-----")
        while True:#输入查找的群ID，不能有空格或者为空
            name = input("请输入群ID: ")
            if name:
                if ' ' in name:
                    print("查找失败")
                    continue
                else:
                    break
            print("ID不能为空")
        msg = '032 ' + self.username + ' ' + name
        sockfd.sendto(msg.encode(),self.addr)
        self.step_2()

    #开始群聊
    def startgroupchat(self):
        sockfd = socket(AF_INET,SOCK_DGRAM)
        msg = '033 ' + self.username
        print("正在发起群聊")
        sockfd.send(msg.encode(),self.addr)
        self.step_2()

    #添加好友
    def addfriend(self):
        sockfd = socket(AF_INET,SOCK_DGRAM)
        print("----|添加好友|:  |  输入ID  |----")
        while True:#输入用户名，不能有空格或者为空
            name = input("请输入ID: ")
            if name:
                if ' ' in name:
                    print("查找失败")
                    continue
                else:
                    break
            print("ID不能为空")
        msg = '031 ' + self.username + ' ' + name
        sockfd.sendto(msg.encode(),self.addr)
        self.step_2()
    
    def modify(self):#修改密码、修改电话号码、修改性别和修改出生日期
        sockfd = socket(AF_INET,SOCK_DGRAM)
        print("------1) 修改密码--------")
        print("------2) 修改电话号码-----")
        print("------3) 修改性别-----")
        print("------4) 修改出生日期-----")
        op = input("input operation: ")
        if op == '1':
            while True:#输入密码，不能有空格、不能为空、不能小于6位、不能全为数字或者字母
                oldpassword = input("请输入旧密码: ")
                if oldpassword:
                    if ' ' in oldpassword:
                        print("密码错误")
                        continue
                    elif len(oldpassword) < 6:
                        print("密码错误")
                        continue
                    elif oldpassword.isdigit():
                        print("密码错误")
                        continue
                    elif oldpassword.isalpha():
                        print("密码错误")
                        continue
                    else:
                        break
                print("密码不能为空")
            while True:#输入密码，不能有空格、不能为空、不能小于6位、不能全为数字或者字母
                newpassword = input("请输入密码: ")
                if newpassword:
                    if ' ' in newpassword:
                        print("不能有空格!!")
                        continue
                    elif len(newpassword) < 6:
                        print("密码不能小于6位数!!")
                        continue
                    elif newpassword.isdigit():
                        print("密码强度弱，不能全为数字")
                        continue
                    elif newpassword.isalpha():
                        print("密码强度弱，不能全为字母")
                        continue
                    else:
                        break
                print("密码不能为空")
            msg = '041 ' + self.username + ' ' + oldpassword + ' ' + newpassword
            sockfd.sendto(msg.encode(),self.addr)
            self.step_2()
        elif op == '2':
            while True:#输入电话号码，必须为11位
                newtel = input("请输入电话号码: ")
                if newtel.isdigit():
                    if len(newtel) != 11:
                        print("正确的11位电话号码!!")
                        continue
                    else:
                        break
                print("电话号码格式错误")
            msg = '042 ' + self.username + ' ' + newtel
            sockfd.sendto(msg.encode(),self.addr)
            self.step_2()
        elif op == '3':
            while True:#输入性别 性别可以为空
                gender = input("请输入性别: ")
                if gender:
                    if gender == 'f' or gender == 'm' or gender == 's':
                        break
                    else:
                        print("请输入正确性别!!")
                        continue
                print("性别不能为空")
            msg = '043 ' + self.username + ' ' + gender
            sockfd.sendto(msg.encode(),self.addr)
            self.step_2()
        elif op == '4':
            while True:#输入出生日期，要求格式xxxx/xx/xx
                birth = input("请输入出生日期(如1999/01/01): ")
                if birth:
                    if len(birth) == 10:
                        if birth[4] !='/' and birth[7] != '/':
                            print("格式错误，请输入xxxx/xx/xx")
                            continue
                        else:
                            break
                    print("格式错误")
                    continue
                print("出生日期不能为空") 
            msg = '044 ' + self.username + ' ' + birth
            sockfd.sendto(msg.encode(),self.addr)
            self.step_2()
        else:
            self.step_2()
            
    def do_login(self,sockfd):#登录操作 用户名和密码都不能有空格，也不能为空
        print("+--------------------------+")
        print("|-|用户名|:|             |--|")
        print("|-|密  码|:|             |--|")
        print("+--------------------------+")
        while True:#输入用户名
            username = input("input username: ")
            if username:
                if ' ' in username:
                    print("用户名不合法!!")
                    continue
                else:
                    break
            print("用户名不能为空!!")
                
        while True:#输入密码
            password = input("input password: ")
            if password:
                if ' ' in password:
                    print("密码错误，请重新输入")
                    continue
                elif len(password) < 6:
                    print("密码错误，请重新输入")
                    continue
                elif password.isdigit():
                    print("密码错误，请重新输入")
                    continue
                elif password.isalpha():
                    print("密码错误，请重新输入")
                    continue
                else:
                    break
            print("密码不能为空")

        msg = '011 ' + username + ' ' + password
        self.username = username
        sockfd.send(msg.encode())
        data = sockfd.recv(1024)
        print(data.decode())
        #发送登录请求后，如果登录成功会收到'011 OK',如果失败会收到'011 Failed'
        if data.decode == '011 OK':
            #登录成功后会收到好友列表
            l = []
            while True:
                data = sockfd.recv(1024)
                if not data:
                    break
                l.append(data.decode())
            print(l)
            #收到好友列表后会有三个线程，一个进行操作，一个发送心跳包，一个一直等待收消息
            t1 = Thread(target = self.step_2,args=())
            t2 = Thread(target = self.heartbeat,args = ())
            t3 = Thread(target = self.Receive,args = ())
            self.Thread_list.append(t1)
            self.function_list.append(t1)
            self.Thread_list.append(t2)
            self.function_list.append(t2)
            self.Thread_list.append(t3)
            self.function_list.append(t3)

            sockfd.close()
            for x in self.function_list:
                x.start()
        else:
            print("用户名或者密码错误")
            self.do_login(sockfd)

    def heartbeat(self):#心跳包，一直发送确保客户端还存在
        while True:
            self.u_sockfd.sendto('000 alive',self.addr)
            if __debug__:
                print("Time: %s" % time.ctime())
            time.sleep(10)        
    
    #收消息
    def Receive(self):
        sockfd = socket(AF_INET,SOCK_DGRAM)
        while True:
            data,ADDR = self.u_sockfd.recvfrom(1024)
            data = data.decode()
            data_list = data.split(" ")
            
            if data_list[0] == '061':
                print("-----------1)同意添加-----------")
                print("-----------2)拒绝添加-----------")
                op = input(">>>")
                if op == '1':
                    msg = '0611 ' + data_list[1] + ' OK'
                    sockfd.sendto(msg.encode(),self.addr)
                elif op == '2':
                    msg = '0612 ' + data_list[1] + ' failed'
                    sockfd.sendto(msg.encode(),self.addr)
                continue
                    
            elif data_list[0] == '063':
                msg = '0631 ' + 'seq=x' + ' ' + data_list[1]
                sockfd.sendto(msg.encode(),self.addr)
                print(data_list[2])
                continue


            elif data_list[0] == '064':
                print("---------1)接收文件--------")
                print("---------2)拒绝文件--------")
                op = input(">>>")

                if op == '1':
                    msg = '0641 ' + data_list[1] + ' OK'
                    sockfd.sendto(msg.encode(),self.data)
                    t_sockfd = socket()
                    t_sockfd.connect(self.addr2)
                    while True:
                        data = t_sockfd.recv(1024)
                        if not data:
                            break
                        print(data.decode())
                    t_sockfd.close()
                    continue
                elif op == '2':
                    msg = '0642 ' + data_list[1] + ' failed'
                    sockfd.sendto(msg.encode(),self.data)
                    continue
            elif data_list[1] == '065':
                print("-----------1)接收图片-----------")
                print("-----------2)拒绝图片-----------")
                op = input(">>>")
                if op == '1':
                    msg = '0651 ' + data_list[1] +' OK'
                    sockfd.sendto(msg.encode(),self.addr)
                    t_sockfd = sockfd()
                    t_sockfd.connect(self.addr2)
                    while True:
                        data = t_sockfd.recv(1024)
                        if not data:
                            break
                        print(data.decode())
                    t_sockfd.close()
                    continue
                elif op == '2':
                    msg = '0652 ' + data_list[1] +' failed'
                    sockfd.sendto(msg.encode(),self.addr)
                    continue

            elif data_list[0] == '066':
                print("---------1)同意进群---------")
                print("---------2)拒绝进群---------")
                op = input(">>>")
                if op == '1':
                    msg = '0661 ' + data_list[1] +' OK'
                    sockfd.sendto(msg.encode(),self.addr)
                    continue
                elif op == '2':
                    msg = '0662 ' + data_list[1] +' failed'
                    sockfd.sendto(msg.encode(),self.addr)
                    continue

    def register(self,sockfd):#注册包括用户名、密码、性别、出生日期和电话号码。性别为选填
        print('+--------------------------+')
        print('|--|用户名|: |              |')
        print('|--|密  码|: |              |')
        print('|--|性  别|: |              |')
        print('|--|出生日期|:|              |')
        print('|--|电话号码|:|              |')
        print('+--------------------------+')
        while True:#输入用户名，不能有空格或者为空
            username = input("请输入用户名: ")
            if username:
                if ' ' in username:
                    print("不能有空格!!")
                    continue
                else:
                    break
            print("用户名不能为空")
                
        while True:#输入密码，不能有空格、不能为空、不能小于6位、不能全为数字或者字母
            password = input("请输入密码: ")
            if password:
                if ' ' in password:
                    print("不能有空格!!")
                    continue
                elif len(password) < 6:
                    print("密码不能小于6位数!!")
                    continue
                elif password.isdigit():
                    print("密码强度弱，不能全为数字")
                    continue
                elif password.isalpha():
                    print("密码强度弱，不能全为字母")
                    continue
                else:
                    break
            print("密码不能为空")

        while True:#输入性别 性别可以为空
            gender = input("请输入性别: ")
            if gender:
                if gender == 'f' or gender == 'm' or gender == 's':
                    break
                else:
                    print("请输入正确性别!!")
                    continue
            break
        
        while True:#输入出生日期，要求格式xxxx/xx/xx
            birth = input("请输入出生日期(如1999/01/01): ")
            if birth:
                if len(birth) == 10:
                    if birth[4] !='/' and birth[7] != '/':
                        print("格式错误，请输入xxxx/xx/xx")
                        continue
                    else:
                        break
                print("格式错误")
                continue
            print("出生日期不能为空")       

        while True:#输入电话号码，必须为11位
            tel = input("请输入电话号码: ")
            if tel.isdigit():
                if len(tel) != 11:
                    print("正确的11位电话号码!!")
                    continue
                else:
                    break
            print("电话号码格式错误")


        msg = '012 ' + username + ' ' + password + ' ' + birth + ' ' + tel +' ' + gender
        sockfd.send(msg.encode())
        sockfd.close()
        self.step_1()


    def forgetpw(self,sockfd):#忘记用户名要求输入用户名和电话号码
        print("+-------------------------------+")
        print("|--|要找回的用户名| ：|         |--|")
        print("|--| 电 话 号 码 | ：|         |--|")
        print("+-------------------------------+")
        while True:#输入用户名，不能有空格或者为空
            name = input("请输入用户名: ")
            if name:
                if ' ' in name:
                    print("不能有空格!!")
                    continue
                else:
                    break
            print("用户名不能为空")

        while True:#输入电话号码，必须为11位
            tel = input("请输入电话号码: ")
            if tel.isdigit():
                if len(tel) != 11:
                    print("正确的11位电话号码!!")
                    continue
                else:
                    break
            print("电话号码格式错误")
        msg = '013 ' + name + ' ' + tel 
        sockfd.send(msg.encode())
        sockfd.close()
        self.step_1()


    def do_quit(self,sockfd):
        msg = '014 ' + self.username
        sockfd.send(msg.encode())
        sockfd.close()
        for x in self.Thread_list:
            x.join()
        sys.exit("quit")

    def menu_quit(self):
        sockfd = socket(AF_INET,SOCK_DGRAM)
        msg = '014 ' + self.username
        sockfd.sendto(msg.encode(),self.addr)

if __name__ == '__main__':
    test = PrivateChatRoomClient()
    test.step_1()
