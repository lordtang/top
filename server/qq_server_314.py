from socket import *
from select import *
from struct import *
import os,sys
import signal
import time
from multiprocessing import Process,Pool
from multiprocessing import Queue
from dboper import *
from udprequest import *
from tcprequest import *
from log import *
from file_server import *
from find_friend import find_friend_server

#全局变量
HOST = '0.0.0.0'
PORT = 8080
ADDR = (HOST,PORT)
#处理僵尸进程
signal.signal(signal.SIGCHLD,signal.SIG_IGN)
#创建epoll字典
g_fdmap = {}
g_fd = None
g_online={}
#定时检查用户在线情况 只会有一个在线字典
queue_online = Queue(1)
queue_online.put(g_online)
#日志路径
path = '/home/ayuan/Top/file_store'
#创建数据库实体类
db_operate =DBOper()
#连接数据库
db_operate.open_conn()

#基于udp套接字用176.209.108.41  广播:176.209.108.255  掩码:255.255.255.0
        #   inet6 地址: fe80::761d收客户端发来消息（心跳包和转发消息）
def udp_server(queue_online):
    #创建udp套接字
    logger.debug("enter {}".format(udp_server.__name__))
    sockfd = socket(AF_INET,SOCK_DGRAM)
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(ADDR)
    while True:
        logger.info("udp服务器8080端口正在监听...")
        data,addr = sockfd.recvfrom(1024)
        data_list = data.decode().split(" ")
        udp_level = Udp_Level(sockfd,data.decode(),addr,db_operate)
        print("connect from",addr)
        print(data_list)
        if data_list[0] == '10086':
            #添加每个用户的udp端口 目的为实现转发消息
            udp_level.insert_udp_addr()
        elif data_list[0] == '031':
            #查找用户，返回给客户端用户信息
            print("查找好友")
            udp_level.find_friend()
        elif data_list[0] == '0310':
            #用户发起加好友请求
            udp_level.add_friend()

        elif data_list[0] == '0311':
            #添加好友请求回复:同意
            print("测试2")
            udp_level.permit_add_friend()
        elif data_list[0] == '0312':
            #添加好友请求回复:拒绝
            udp_level.refuse_add_friend()
        elif data_list[0] == '032':
            #添加群聊请求 032 user_id groupid 
            pass
        # elif data_list[0] =='0661':
        #     #添加群聊请求 同意
        #     pass
        # elif data_list[0] == '0662':
        #     #添加群聊请求 拒绝
        #     pass
        elif data_list[0] == '033':
            #发起群聊请求 033 user_id
            pass
        elif data_list[0] == '034':
            #修改个人信息 034 包括 修改密码 修改电话号码 修改性别 修改出生日期 user_id
            udp_level.update_user_info()
        elif data_list[0] == '014':
            #退出 user_name
            pass
        elif data_list[0] == '036':
            #发消息  035 text #seq=x
            udp_level.send_message()
        elif data_list[0] == '063':
            #发消息回复
            udp_level.ack_message()

        elif data_list[0] == '038':
            print("客户端传来一个文件")
            # udp_level.send_file()

        elif data_list[0] == '0642':
            #c2拒绝接收文件或者中断文件传输
            pass

        elif data_list[0] == '06411':
            #c1客户端完成发送，c2该接收文件了
            print('收到06411')
            udp_level.file_finish()

        elif data_list[0] == '065':
            udp_level.send_pic()
        
        elif data_list[0] == '0651':
            print('收到0651')
            udp_level.pic_finish()

        elif data_list[0] == '041':
            #修改密码 041 oldpasswd newpassword
            udp_level.modify_passwd()
        elif data_list[0] == '042':
            #修改电话号码 042 newtel
            udp_level.modify_tel_no()
        elif data_list[0] =='043':
            #修改性别 043 gender
            udp_level.modify_gender()
        elif data_list[0] == '044':
            #修改出生日期 044 birth
            udp_level.modify_birthdate()
        elif data_list[0] == '045':
            #消息免打扰 045 这个应该客户端的应用层做保证吧 服务器依然会发消息
            pass
        elif data_list[0] == '000':
            #客户端报活  更新数据库lasttimen字段 000 alive 
            # udp_level.keep_alive(queue_online)
            pass
        elif data_list[0] == '051':
            #客户端收到方确认包 直接转发 不做任何处理 ack =x
            pass

        elif data_list[0] == '066':
            #客户端请求语音聊天
            udp_level.voice_chat_request()

        elif data_list[0] == '0661':
            #请求语音聊天回复 同意
            udp_level.promise_achat()

        elif data_list[0] == '0662':
            #中断语音聊天的回复
            udp_level.interupt_achat()

        elif data_list[0] == '067':
            #客户端请求视频聊天
            udp_level.video_chat_request()

        elif data_list[0] == '0671':
            #请求视频聊天回复 同意
            udp_level.promise_vchat()
            
        elif data_list[0] == '0672':
            #中断视频聊天的回复
            udp_level.interupt_vchat()
    

#基于tcp套接字和基于epoll实现并发 连接登录请求
def tcp_server():
    #创建tcp套接字
    logger.debug("enter {}".format(tcp_server.__name__))
    sockfd = socket(AF_INET,SOCK_STREAM)
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(ADDR)
    sockfd.listen(10)
    logger.info("tcp服务器8080端口正在监听...")
    #创建epoll对象
    p = epoll()
    g_fdmap = {sockfd.fileno():sockfd}
    p.register(sockfd,EPOLLIN|EPOLLERR)
    #循环监控
    while True:
        try:
            events = p.poll()
        except KeyboardInterrupt:
            sys.exit("服务器退出")
        #遍历列表，处理IO
        for fd,event in events:
            if fd == sockfd.fileno():
                conn,addr = g_fdmap[fd].accept()
                logger.info("Connect from {}{}".format(addr[0],addr[1]))
                #添加新的注册IO
                p.register(conn,EPOLLIN|EPOLLHUP)
                g_fdmap[conn.fileno()] = conn
            else:
                # 使用struct解决粘包的问题
                # pack_data = g_fdmap[fd].recv(4)
                # fmt = 'i'
                # header  = struct.Struct(fmt)
                # length = header.unpack(pack_data)[0]
                try:
                    request_data = g_fdmap[fd].recv(1024)
                except ConnectionResetError:
                    g_fdmap[fd].close()
                    del g_fdmap[fd]
                    continue
                print(request_data)
                #如果客户端非正常断开
                if not request_data:
                    #更新字典
                    g_fdmap[fd].close()
                    del g_fdmap[fd]
                    continue
                handle_request(fd,g_fdmap[fd],request_data,addr,db_operate)

#用于处理客户端各种请求
def handle_request(fd,conn,request_data,addr,db_operate):
    #解析request_data
    data = request_data.decode()
    data_list = data.split(' ')
    cmd = data_list[0]
    #实例化一个处理一级界面
    first_level = First_Level(fd,conn,request_data,data,addr,db_operate)
    if cmd == '011':
        #登录请求
        first_level.do_login()
    elif cmd == '012':
        #注册请求
        first_level.do_register()
    elif cmd == '0121':
        #名字先测试 0121 user_id
        first_level.do_check_name()
    elif cmd == '013':
        #忘记密码请求
        first_level.do_find_passwd()
    elif cmd == '0131':
        # 0131 user_id
        first_level.do_find_passwd_info() 
    elif cmd == '014':
        #退出请求(登录失败或者注册失败后退出)pass
        first_level.do_quit()
#服务器检查客户端存活状态
def check_alive(sec,conn,q):
    check_heart(sec,conn,q)
    #定时任务 用schedue


if __name__ == "__main__":
    print("start....")
    p1 = Process(target = tcp_server)
    p2 = Process(target = udp_server,args=(queue_online,))
    # p3 = Process(target = check_alive,args = (45,db_operate,q))
    p4 = Process(target = file_server)
    p5 = Process(target = find_friend_server,args=(db_operate,))
    p2.daemon = True
    # p3.daemon = True
    #保护进程不可以有子进程
    # p4.daemon = True
    p1.start()
    p2.start()
    # p3.start()
    p4.start()
    p5.start()
    p1.join()
    #进程结束时关闭数据库
    db_operate.close_conn()
    