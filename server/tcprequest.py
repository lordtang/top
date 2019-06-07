import time
import struct
from log import *
class First_Level():
    def __init__(self,fd,conn,request_data,content,addr,db_operate):
        self.fd = fd
        self.conn = conn
        #未解码的数据
        self.request_data = request_data
        self.content = content.strip()
        self.addr = addr
        self.ip = addr[0]
        self.port = addr[1]
        self.db_operate = db_operate
    def do_login(self):
        #客户端消息格式：user_id + passwd
        content_list = self.content.split(' ')
        length = len(content_list)
        print(length)
        if length < 3:
            try:
                self.conn.send(b'011 Failed')
            except ConnectionResetError:
                return
            logger.info("send message:011 Failed to {}{}".format(self.ip,self.port))
            return
        user_id = int(content_list[1])
        passwd = content_list[2]  
        #查询用户号码和密码是否匹配 查询返回的data是元组 或者None
        flag = 0
        sql =  "select * from user_tbl where user_id = %d and passwd = '%s'"%(user_id,passwd)
        data = self.db_operate.do_sql(sql,flag)
        logger.info("执行sql语句:{}".format(sql))
        # print("查询登录结果:",data)
        if not data:
            try:
                self.conn.send(b'011 Failed')
            except ConnectionResetError:
                return
            logger.info("send message:011 Failed to {}{}".format(self.ip,self.port))
            return      
        else:
            try:
                self.conn.send(b'011 OK')
                logger.info("send message:011 OK to {}{}".format(self.ip,self.port))
            except ConnectionResetError:
                return
            time.sleep(1)
            flag1 = 1
            #好友实体friends 返回friend_id 和　user_id 并更新user_ip user_tcp_port 还有暂存个人消息和群消息　发送成功后删除数据库
            sql_update = "update user_tbl set user_stat = '1',user_ip = '%s',user_tcp_port = '%s' where user_id = %d"%(self.ip,self.port,user_id)
            logger.info("执行sql语句:{}".format(sql_update))
            # print(sql_update)
            data_status = self.db_operate.do_sql(sql_update,flag1)
            if not data_status:
                try:
                    self.conn.send(b'011 Failed')
                except ConnectionResetError:
                        return
                logger.info("send message:011 Failed to {}{}".format(self.ip,self.port))
                return
            # 本人信息
            flag = 0
            sql = "select user_name,user_tel,brith,gender,logo from user_tbl where user_id = %d"%user_id
            user_info = self.db_operate.do_sql(sql,flag)
            print(user_info)
            logo = user_info[0][4]
            print(logo)
            sql_logo = "select logo_pic from user_logo where id =%d"%logo
            logo_info = self.db_operate.do_sql(sql_logo,flag)
            logo_bytes = logo_info[0][0]
            #struct包
            fmt = 'i'
            header  = struct.Struct(fmt)
            length = len(str(user_id).encode())
            pack_id = header.pack(length)
            self.conn.send(pack_id)
            self.conn.send(str(user_id).encode())

            for i in range(4):
                print(user_info[0][i])
                length = len(user_info[0][i].encode())
                print(length)
                pack_data = header.pack(length)
                self.conn.send(pack_data)
                self.conn.send(user_info[0][i].encode())
            
            pack_logo = header.pack(len(logo_bytes))
            self.conn.send(pack_logo)
            self.conn.send(logo_bytes)

            #本人基本信息和好友基本信息 分割线为###
            pack_line = header.pack(3)
            self.conn.send(pack_line)
            self.conn.send(b'###')

            #好友id name logo
            flag = 0
            sql = "select friend_id from user_friends where owner_id = %d"%user_id
            logger.info("执行sql语句:{}".format(sql))
            #二维元组
            friends = self.db_operate.do_sql(sql,flag)
            length_friends = len(friends)
            i = 1
            print("Friends：",friends)
            if not friends:
                pack_name = header.pack(3)
                self.conn.send(pack_name)
                self.conn.send(b'new')
            for friend in friends:
                friend_id = friend[0]
                #获取好友信息
                flag = 0
                sql = "select user_name,logo from user_tbl where user_id = %d"%friend_id
                friend_info = self.db_operate.do_sql(sql,flag)
                print(friend_info)
                logo = friend_info[0][1]
                #获取好友头像信息
                sql_logo = "select logo_pic from user_logo where id =%d"%logo
                friend_logo_info = self.db_operate.do_sql(sql_logo,flag)
                friend_logo_bytes = friend_logo_info[0][0]

                #发送好友id
                pack_id = header.pack(len(str(friend_id).encode()))
                self.conn.send(pack_id)
                self.conn.send(str(friend_id).encode())

                #发送好友名字
                print(friend_info[0][0])
                length = len(friend_info[0][0].encode())
                pack_name = header.pack(length)
                self.conn.send(pack_name)
                self.conn.send(friend_info[0][0].encode())

                #发送好友头像信息
                pack_logo = header.pack(len(friend_logo_bytes))
                self.conn.send(pack_logo)
                self.conn.send(friend_logo_bytes)
                if i < length_friends:
                    #好友基本信息与好友基本信息之间 分割线为## 最后一次就不再发送##而是发送***
                    pack_line = header.pack(2)
                    self.conn.send(pack_line)
                    self.conn.send(b'##')
                    i += 1
            
            #好友基本信息与暂存信息之间 分割线为***(最后一个元素会多一个分割线)
            pack_line = header.pack(3)
            self.conn.send(pack_line)
            self.conn.send(b'***')
            # #user暂存消息 包括好友请求 群主还有加群请求 好友消息 私聊临时消息 收到确认后将暂存消息删除
            # logger.info("向登录成功的用户发送好友信息　暂存个人消息和群消息　用户名为{}{}".format(self.ip,self.port))
            #返回一个确认收到消息 
        return

    def do_check_name(self):
        #查找昵称是否重复　客户端消息格式user_name
        print(self.content)
        content_list = self.content.split(' ')
        length = len(content_list)
        if length < 2:
            try:
                self.conn.send(b'0121 Failed') 
            except ConnectionResetError:
                return
            logger.info("send message:0121 Failed to {}{}".format(self.ip,self.port))
            return
        user_name = content_list[1]
        # print("客户端注册姓名",user_name)
        flag = 0
        sql =  "select * from user_tbl where user_name = '%s'"%(user_name)
        logger.info("执行sql语句:{}".format(sql))
        data = self.db_operate.do_sql(sql,flag)
        # print(data)
        if not data:
            try:
                self.conn.send(b'0121 OK')
            except ConnectionResetError:
                return
            logger.info("send message:0121 OK to {}{}".format(self.ip,self.port))
            return
        else:
            try:
                self.conn.send(b'0121 Failed')
            except ConnectionResetError:
                return
            logger.info("send message:0121 Failed to {}{}".format(self.ip,self.port))

    def do_register(self):
        #注册包括用户名、密码、性别(3)、出生日期 电话号码。性别为选填 
        # print("注册内容:",self.content)
        content_list = self.content.split(' ')
        length = len(content_list)
        if length < 6:
            try:
                self.conn.send(b'012 Failed Failed') 
            except ConnectionResetError:
                return
            logger.info("send message:012 Failed Failed to {}{}".format(self.ip,self.port))
            return
        user_name = content_list[1]
        passwd = content_list[2]
        gender = content_list[3]
        birth =  content_list[4]
        user_tel = content_list[5]
        # user_name = content_list[1]
        # passwd = content_list[2]
        # gender = content_list[5]
        # birth =  content_list[3]
        # user_tel = content_list[4]
        #查询用户名 电话号码是否有重复
        flag = 0
        sql =  "select * from user_tbl where user_name = '%s' or user_tel = '%s'"%(user_name,user_tel)
        logger.info("执行sql语句:{}".format(sql))
        data = self.db_operate.do_sql(sql,flag)
        print(data)
        if not data:
            flag = 1
            #注册成功后，将注册信息插入数据库 (添加注册时间字段 修改last_time数据类型 datetime) 添加语句返回1或者0
            sql_insert_info = "insert into user_tbl(user_name,passwd,gender,brith,user_tel,user_stat,user_ip, user_tcp_port,last_time) values('%s','%s','%s','%s','%s','1','%s','%s',now())"%(user_name,passwd,gender,birth,user_tel,self.ip,self.port)
            logger.info("执行sql语句:{}".format(sql_insert_info))
            data = self.db_operate.do_sql(sql_insert_info,flag)
            if not data:
                print("添加用户信息失败！")
                try:
                    self.conn.send(b'012 Failed Failed')
                except ConnectionResetError:
                    return
                logger.info("send message:012 Failed Failed to {}{}".format(self.ip,self.port))
            else:
                print("添加用户信息成功！")
                #注册信息成功后返回user_id
                flag = 0
                sql =  "select user_id from user_tbl where user_name = '%s'"%(user_name)
                print(sql)
                data_info = self.db_operate.do_sql(sql,flag)
                print(data_info)
                user_id = data_info[0][0]
                send_msg = '012 OK ' + str(user_id)
                try:
                    self.conn.send(send_msg.encode())
                except ConnectionResetError:
                    return
                logger.info("send message:012 OK {} to {}{}".format(user_id,self.ip,self.port))
        else:
            try:
                self.conn.send(b'012 Failed Failed')
            except ConnectionResetError:
                return
            logger.info("send message:012 Failed Failed to {}{}".format(self.ip,self.port))
        return

    def do_find_passwd_info(self):
        #客户端发来的消息为　user_id
        content_list = self.content.split(' ')
        length = len(content_list)
        if length < 2:
            try:
                self.conn.send(b'0131 Failed 0') 
            except ConnectionResetError:
                return
            logger.info("send message:012 Failed 0 to {}{}".format(self.ip,self.port))
            return
        user_id = int(content_list[1])
        #查询user_id 并返回电话号码
        flag = 0
        sql =  "select user_tel from user_tbl where user_id = %d"%(user_id)
        logger.info("执行sql语句:{}".format(sql))
        data = self.db_operate.do_sql(sql,flag)
        print(data)
        if not data:
            try:
                self.conn.send(b'0131 Failed 0')
            except ConnectionResetError:
                return
            logger.info("send message:012 Failed 0 to {}{}".format(self.ip,self.port))  
        else:
            #取返回值中的电话号码
            send_msg = '0131 OK ' + data[0][0]
            try:
                self.conn.send(send_msg.encode())
                # print("测试发送0131 Ok")
            except ConnectionResetError:
                return
            logger.info("send message:012 Failed {} to {}{}".format(data[0][0],self.ip,self.port))
        return  
 
    def do_find_passwd(self):
        content_list = self.content.split(' ')
        length = len(content_list)
        if length < 3:
            try:
                self.conn.send(b'013 Failed') 
            except ConnectionResetError:
                return
            logger.info("send message:013 Failed to {}{}".format(self.ip,self.port))
            return 
        user_id = int(content_list[1])
        new_passwd = content_list[2]
        #查询用户名和电话号码是否一致
        flag = 0
        sql =  "select * from user_tbl where user_id = %d"%(user_id)
        data = self.db_operate.do_sql(sql,flag)
        if not data:
            try:
                self.conn.send(b'013  Failed')
            except ConnectionResetError:
                return
            logger.info("send message:013 Failed to {}{}".format(self.ip,self.port))  
        else:
            #更新数据库密码
            flag = 1
            sql = "update user_tbl set passwd = '%s' where user_id = %d"%(new_passwd,user_id)
            logger.info("执行sql语句:{}".format(sql))
            data = self.db_operate.do_sql(sql,flag)
            if not data:
                try:
                    self.conn.send(b'013  Failed')
                except ConnectionResetError:
                    return
                logger.info("send message:013 Failed to {}{}".format(self.ip,self.port))
            else:
                try:
                    self.conn.send(b'013 OK')
                except ConnectionResetError:
                    return
                logger.info("send message:013 OK to {}{}".format(self.ip,self.port))
        return

    def do_quit(self):
        # 更新字典
        # print(g_fdmap)
        self.conn.close()
        del self.conn
        logger.info("close {}{}".format(self.ip,self.port))
        # print(g_fdmap)

    def do_friend_list(self):
        pass
