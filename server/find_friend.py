from socket import *
from struct import Struct
from log import *
from dboper import DBOper
import os,sys
from threading import Thread

from multiprocessing import Pool,Process

path = '/home/ayuan/Top/file_store'


def find_friend_server(dbopenr):
    server = socket()
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 6970))  # 绑定监听端口
    server.listen(5)  # 监听
    logger.info("好友请求服务器正在监听..")
    while True:
        try:
            conn,addr = server.accept()  # 等待连接
        except Exception as e:
            logger.info('Error:{}'.format(e))
            continue

        logger.info("conn:{}\naddr:{}".format(conn, addr))  # conn连接实例
        th = Thread(target=handle,args=(conn,dbopenr))
        th.setDaemon(True)
        th.start()


def handle(conn,dbopenr):
    print("开始处理函数")
    try:
        data = conn.recv(1024)  # 接收
    except Exception as e:
        logger.info('Error:{}'.format(e))
    if not data:  # 客户端已断开
        logger.info("客户端断开连接\r\n")
        return
    
    logger.info("请求的好友id：{}".format(data.decode("utf-8")))
    ids = data.decode().split('#')
    fmt = 'i'
    header  = Struct(fmt)
    for i in ids:
        friend_id = int(i)
        #获取好友信息
        flag = 0
        while True:
            try:
                sql = "select user_name,brith,gender,logo from user_tbl where user_id = %d"%friend_id
            except Exception:
                pass
            friend_info = dbopenr.do_sql(sql,flag)
            if friend_info:
                break
            else:
                continue
        print('friend_info:',friend_info)
        logo = friend_info[0][3]
        #获取好友头像信息
        sql_logo = "select logo_pic from user_logo where id =%d"%logo
        friend_logo_info = dbopenr.do_sql(sql_logo,flag)
        friend_logo_bytes = friend_logo_info[0][0]

        #发送好友id
        pack_id = header.pack(len(str(friend_id).encode()))
        conn.send(pack_id)
        conn.send(str(friend_id).encode())

        #发送好友名字
        length = len(friend_info[0][0].encode())
        pack_name = header.pack(length)
        conn.send(pack_name)
        conn.send(friend_info[0][0].encode())

        #发送好友出生日期
        length = len(friend_info[0][1].encode())
        pack_birth = header.pack(length)
        conn.send(pack_birth)
        conn.send(friend_info[0][1].encode())

        #发送好友性别
        length = len(friend_info[0][2].encode())
        pack_gender = header.pack(length)
        conn.send(pack_gender)
        conn.send(friend_info[0][2].encode())

        #发送好友头像信息
        pack_logo = header.pack(len(friend_logo_bytes))
        print(len(friend_logo_bytes))
        conn.send(pack_logo)
        conn.send(friend_logo_bytes)

        pack_line = header.pack(2)
        conn.send(pack_line)
        conn.send(b'##')
            
    #好友基本信息与暂存信息之间 分割线为***(最后一个元素会多一个分割线)
    pack_line = header.pack(3)
    conn.send(pack_line)
    conn.send(b'***')
