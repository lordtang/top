import os
import time
import datetime
from create_sql import get_sql
class Udp_Level():
    def __init__(self,sockfd,data,addr,db_operate):
        self.sockfd = sockfd
        self.data = data
        self.addr = addr
        self.db_operate = db_operate


    def insert_udp_addr(self):
        data_list = self.data.split(' ')
        if len(data_list) < 2:
            return
        user_id = int(data_list[1])
        flag = 1
        sql = "update user_tbl set user_udp_port ='%s' where user_id = %d"%(self.addr[1],user_id)
        data = self.db_operate.do_sql(sql,flag)
        if not data:
            print("添加udp端口失败。。。")
        else:
            print("添加udp端口成功。。。。")

    def find_friend(self):
        data_list = self.data.split(' ')
        user_id = int(data_list[1])
        try:
            friend_user_idorname = int(data_list[2])
        except:
            friend_user_idorname = data_list[2]
        gender = data_list[3]
        age = data_list[4]
        flag = 0
        sql = get_sql(friend_user_idorname,gender,age)
        friend_data_info = self.db_operate.do_sql(sql,flag)
        sql = "select user_stat,user_ip,user_udp_port from user_tbl where user_id = %d"%int(user_id)
        user_data_info = self.db_operate.do_sql(sql,flag)
        if not friend_data_info:
            if user_data_info[0][0] == '1':
                user_addr = (user_data_info[0][1],user_data_info[0][2])
                send_msg = '031 ' + 'False'
                self.sockfd.sendto(send_msg.encode(),user_addr)
                print('未查找到好友')
            # 在线就发，不在线情况暂时不做处理
            else:
                pass
        else:
            if user_data_info[0][0] == '1':
                user_addr = (user_data_info[0][1],user_data_info[0][2])
                ids = ''
                for i in friend_data_info:
                    ids += (str(i[0]) + '#')
                ids = ids.rstrip('#')
                send_msg = '031 ' + '%s'%ids
                self.sockfd.sendto(send_msg.encode(),user_addr)
                print('查找到好友')
            # 在线就发，不在线情况暂时不做处理
            else:
                pass



    def add_friend(self):
        print("有用户添加好友。。。。")
        data_list = self.data.split(' ')
        user_id = int(data_list[1])
        friend_user_id = int(data_list[2])
        #查找该用户是否存在
        flag = 0
        sql = "select user_stat,user_ip,user_udp_port from user_tbl where user_id = %d"%friend_user_id
        #username是唯一的,要不没有数据,要不只有一条数据
        data_info = self.db_operate.do_sql(sql,flag)
        print("查询数据：",data_info)
        if not data_info:
            #如果该用户不存在不做任何处理
            return
        else:
            #请求好友的status ip port
            if data_info[0][0] == '1':
                friend_addr = (data_info[0][1],data_info[0][2])
                print(friend_addr)
                send_msg = '0310 '+ str(user_id) + ' ' + str(friend_user_id)
                self.sockfd.sendto(send_msg.encode(),friend_addr)
                # self.sockfd.sendto(b'0611 OK',self.addr) 
            else:
                print("向数据库消息记录表插入0条记录")
                #向数据库消息记录表插入一条记0
                #send_user recv_user 文件地址/消息内容 time 
                flag = 1
                content = '0310 '+ str(user_id) + ' ' + str(friend_user_id)
                sql = "insert into user_msg_content(send_user_id,recv_user_id,content,send_time) values(%d,%d,'%s',now())"%(user_id,friend_user_id,content)
                update_status = self.db_operate.do_sql(sql,flag)
                if not update_status:
                    print("插入信息记录失败")
                    # self.sockfd.sendto(b'0611 Failed',self.addr) 
                    return
                else:
                    print("插入消息记录成功")
                    # self.sockfd.sendto(b'0611 OK',self.addr)
            return

    def permit_add_friend(self):
        data_list = self.data.split(' ')
        print('data_list:',data_list)
        friend_user_id = int(data_list[1])
        user_id = int(data_list[2])
        #查找该用户是否存在
        flag = 0
        sql = "select user_stat,user_ip,user_udp_port from user_tbl where user_id = %d"%friend_user_id
        #username是唯一的,要不没有数据,要不只有一条数据
        data_info = self.db_operate.do_sql(sql,flag)
        print("用户存在：",data_info)
        if not data_info:
            #如果该用户不存在不做任何处理
            return
        else:
            #如果同意添加好友后 更新好友实体 添加两条记录 friend_name owner
            flag = 1
            while True:
                sql = "insert into user_friends(friend_id,owner_id,join_date) values('%s','%s',now())"%(user_id,friend_user_id)
                update_status = self.db_operate.do_sql(sql,flag)
                if update_status:
                    print("插入好友实体信息记录成功")
                    break
            while True:
                sql_friend = "insert into user_friends(friend_id,owner_id,join_date) values('%s','%s',now())"%(friend_user_id,user_id)
                update_status_firend = self.db_operate.do_sql(sql_friend,flag)
                if not update_status_firend:
                    print("插入好友实体信息记录成功")
                    break
                
        if data_info[0][0] == '1':
            print("好友在线哦。。。")
            friend_addr = (data_info[0][1],data_info[0][2])
            msg = '0311 ' + str(user_id)
            self.sockfd.sendto(msg.encode(),friend_addr)
            print("添加好友完毕========")
        else:
            # print("好友不在线哦。。。")
            # print("向数据库消息记录表插入一条记录")
            # #向数据库消息记录表插入一条记录
            # #send_user recv_user 文件地址/消息内容 time
            # flag = 1
            # content = '0611 '+ str(user_id) + ' ' + str(friend_user_id)
            # sql = "insert into user_msg_content(send_user_id,recv_user_id,content,send_time) values(%d,%d,'%s',now())"%(user_id,friend_user_id,content)
            # print(sql)
            # update_status = self.db_operate.do_sql(sql,flag)
            # if not update_status:
            #     self.sockfd.sendto(b'0611 Failed',self.addr)
            #     print("插入信息记录失败")
            #     return
            # else:
            #     friend_addr = (data_info[0][1],data_info[0][2])
            #     print("好友ip端口地址:",friend_addr)
            #     print("本人ip端口地址：",self.addr)
            #     self.sockfd.sendto(b'0611 OK',friend_addr)
            #     self.sockfd.sendto(b'0611 OK',self.addr) 
            #     print("插入消息记录成功")
            pass
        return

    def refuse_add_friend(self):
        #拒绝添加好友请求  不做任何处理
        # self.sockfd.sendto(b'061 OK',self.addr) 
        return

    def add_group(self):
        pass

    def ask_group(self):
        pass

    def update_user_info(self):
        pass

    def quit_login(self):
        pass

    def ack_message(self):
        #对这条消息也不再回复确认
        #发送方发送的消息 063 user_id send_user_id msg #seq=x
        #服务器处理后转发格式：063 user_id send_user_id msg #seq=x
        data_list = self.data.split(' ')
        length = len(data_list)
        if length < 4:
            # self.sockfd.sendto(b'063 Failed',self.addr) 
            return
        user_id = int(self.data.split(' ')[2])
        friend_user_id = int(self.data.split(' ')[1])
        flag = 0
        sql = "select user_stat,user_ip,user_udp_port from user_tbl where user_id = %d"%friend_user_id
        #username是唯一的,要不没有数据,要不只有一条数据
        data_info = self.db_operate.do_sql(sql,flag)
        if not data_info:
            #如果该用户不存在不做任何处理
            self.sockfd.sendto(b'063 Failed',self.addr) 
            return
        else:
            #请求好友的status ip port
            if data_info[0][0] == '1':
                friend_addr = (data_info[0][1],data_info[0][2])
                print("消息回复确认　发送消息朋友addr",friend_addr)
                #服务器不做任何处理直接进行转发　对这条消息也不再回复确认
                send_msg = self.data
                # self.sockfd.sendto(b'063 OK',self.addr) 
                self.sockfd.sendto(send_msg.encode(),friend_addr)
                print("063 OK")
            else:
                print("向数据库消息记录表插入一条记录")
                #向数据库消息记录表插入一条记录
                #send_user recv_user 文件地址/消息内容 time 
                flag = 1
                #服务器不做任何处理
                content = self.data
                sql = "insert into user_msg_content(send_user_id,recv_user_id,content,send_time) values(%d,%d,'%s',now())"%(user_id,friend_user_id,content)
                update_status = self.db_operate.do_sql(sql,flag)
                if not update_status:
                    print("插入信息记录失败")
                    # self.sockfd.sendto(b'063 Failed',self.addr) 
                    return
                else:
                    print("插入消息记录成功")
                    # self.sockfd.sendto(b'063 OK',self.addr) 
                    return

    def send_message(self):
        #发送方发送的消息 036 user_id send_user_id msg#seq=x
        #接受正确消息格式　data + OK 接受错误消息格式　data + Failed
        #服务器处理后转发格式：063 user_id send_user_id(//*//#)msg#seq=x
        print("接受到客户端发来消息。。。",self.data)
        data_list = self.data.split(' ')
        length = len(data_list)
        if length < 5:
            send_msg = self.data + 'Failed'
            self.sockfd.sendto(send_msg.encode(),self.addr)
            return
        user_id = int(self.data.split(' ')[1])
        friend_user_id = int(self.data.split(' ')[2])
        flag = 0
        sql = "select user_stat,user_ip,user_udp_port from user_tbl where user_id = '%s'"%friend_user_id
        #username是唯一的,要不没有数据,要不只有一条数据
        data_info = self.db_operate.do_sql(sql,flag)
        if not data_info:
            #如果该用户不存在不做任何处理
            # self.sockfd.sendto(b'036 Failed',self.addr)
            send_msg = self.data + 'Failed'
            self.sockfd.sendto(send_msg.encode(),self.addr)
            return
        else:
            #请求好友的status ip port
            if data_info[0][0] == '1':
                friend_addr = (data_info[0][1],data_info[0][2])
                print("发送方请求发送消息朋友addr",friend_addr)
                #按照原来的方式进行拼接
                send_recv_msg = '063 ' + data_list[1] + ' ' + data_list[2] +'//*//#'+' '.join(data_list[3:])
                send_msg= self.data + 'OK'
                #发给发送方消息
                self.sockfd.sendto(send_msg.encode(),self.addr)
                #将信息处理后转发给接受方
                self.sockfd.sendto(send_recv_msg.encode(),friend_addr)
                print("发给发送方消息:",send_msg)
                print("接受方地址：",friend_addr)
                print("发给接受方的内容：",send_recv_msg)
            else:
                print("向数据库消息记录表插入一条记录")
                #向数据库消息记录表插入一条记录
                #send_user recv_user 文件地址/消息内容 time 
                flag = 1
                content =  '063 ' + ' '.join(data_list[2:])
                sql = "insert into user_msg_content(send_user_id,recv_user_id,content,send_time) values(%d,%d,'%s',now())"%(user_id,friend_user_id,content)
                update_status = self.db_operate.do_sql(sql,flag)
                if not update_status:
                    print("插入信息记录失败")
                    send_msg = self.data + 'Failed'
                    self.sockfd.sendto(send_msg.encode(),self.addr) 
                    return
                else:
                    print("插入消息记录成功")
                    send_msg = self.data + 'OK'
                    self.sockfd.sendto(send_msg.encode(),self.addr) 
                    return

    def send_file(self):
        data_list = self.data.split(' ')
        print(data_list)
        length = len(data_list)
        if length < 3:
            try:
                self.sockfd.sendto(b'038 Failed',self.addr) 
            except ConnectionResetError:
                return
            return
        user_id = int(self.data.split(' ')[1])
        friend_user_id = int(self.data.split(' ')[2])
        file_name = self.data.split(' ')[3]
        #查找该用户是否存在
        flag = 0
        sql = "select user_stat,user_ip,user_udp_port from user_tbl where user_id = %d"%friend_user_id
        #user_id是唯一的,要不没有数据,要不只有一条数据
        data_info = self.db_operate.do_sql(sql,flag)
        if not data_info:
            #如果该用户不存在不做任何处理
            return
        else:
            #请求好友的status ip port
            if data_info[0][0] == '1':
                friend_addr = (data_info[0][1],data_info[0][2])
                print(friend_addr)
                send_msg = '038 ' + str(user_id) + ' ' + str(friend_user_id) +' '+ file_name
                print(send_msg)
                self.sockfd.sendto(send_msg.encode(),friend_addr)
                print('发送成功')
            else:
                print("向数据库消息记录表插入一条记录")
                #向数据库消息记录表插入一条记录
                #send_user recv_user 文件地址/消息内容 time 
                flag = 1
                content = '064 '+ str(user_id) + ' ' + str(friend_user_id) +file_name
                sql = "insert into user_msg_content(send_user_id,recv_user_id,content,send_time) values(%d,%d,'%s',now())"%(user_id,friend_user_id,content)
                update_status = self.db_operate.do_sql(sql,flag)
                if not update_status:
                    print("插入信息记录失败")
                    self.sockfd.sendto(b'038 Failed',self.addr) 
                    return
                else:
                    print("插入消息记录成功")
                    # self.sockfd.sendto(b'038 OK'.self.addr) 
            return
    

        pass
    
    def file_finish(self):
        data_list = self.data.split(' ')
        length = len(data_list)
        if length < 4:
            try:
                self.sockfd.sendto(b'06411 Failed',self.addr) 
            except ConnectionResetError:
                return
            return
        user_id = int(self.data.split(' ')[1])
        friend_user_id = int(self.data.split(' ')[2])
        file_name = ''.join(self.data.split(' ')[3:])
        file_size = str(os.path.getsize('temp_transend_files/'+file_name))
        #查找该用户是否存在
        flag = 0
        sql = "select user_stat,user_ip,user_udp_port from user_tbl where user_id = %d"%friend_user_id
        #username是唯一的,要不没有数据,要不只有一条数据
        data_info = self.db_operate.do_sql(sql,flag)
        if data_info[0][0] == '1':
            friend_addr = (data_info[0][1],data_info[0][2])
            print('地址信息',friend_addr)
            send_msg = '038 ' + str(user_id) + ' ' + str(friend_user_id) + ' ' + file_name + ' ' + file_size
            self.sockfd.sendto(send_msg.encode(),friend_addr)
            print('发送038成功')
        # 在线就发，不在线情况暂时不做处理
        else:
            print('不在线')
                       
    def send_pic(self):
        data_list = self.data.split(' ')
        length = len(data_list)
        if length < 3:
            try:
                self.sockfd.sendto(b'038 Failed',self.addr) 
            except ConnectionResetError:
                return
            return
        user_id = int(self.data.split(' ')[1])
        friend_user_id = int(self.data.split(' ')[2])
        file_name = self.data.split(' ')[3] + " " +self.data.split(' ')[4]
        #查找该用户是否存在
        flag = 0
        sql = "select user_stat,user_ip,user_udp_port from user_tbl where user_id = %d"%user_id
        #username是唯一的,要不没有数据,要不只有一条数据
        data_info = self.db_operate.do_sql(sql,flag)
        if not data_info:
            #如果该用户不存在不做任何处理
            return
        else:
            if data_info[0][0] == '1':
                addr = (data_info[0][1],data_info[0][2])
                print(addr)
                send_msg = '065 ' + str(user_id) + ' ' + str(friend_user_id) +' '+ file_name
                print(send_msg)
                self.sockfd.sendto(send_msg.encode(),addr)
                print('发送成功')
            else:
                print("向数据库消息记录表插入一条记录")
                #向数据库消息记录表插入一条记录
                #send_user recv_user 文件地址/消息内容 time 
                flag = 1
                content = '065 '+ str(user_id) + ' ' + str(friend_user_id) +file_name
                sql = "insert into user_msg_content(send_user_id,recv_user_id,content,send_time) values(%d,%d,'%s',now())"%(user_id,friend_user_id,content)
                update_status = self.db_operate.do_sql(sql,flag)
                if not update_status:
                    print("插入信息记录失败")
                    self.sockfd.sendto(b'038 Failed',self.addr) 
                    return
                else:
                    print("插入消息记录成功")
                    # self.sockfd.sendto(b'038 OK'.self.addr) 
            return
        
    def pic_finish(self):
        data_list = self.data.split(' ')
        length = len(data_list)
        if length < 4:
            try:
                self.sockfd.sendto(b'0651 Failed',self.addr) 
            except ConnectionResetError:
                return
            return
        user_id = int(self.data.split(' ')[1])
        friend_user_id = int(self.data.split(' ')[2])
        file_name = self.data.split(' ')[3]
        #查找该用户是否存在
        flag = 0
        sql = "select user_stat,user_ip,user_udp_port from user_tbl where user_id = %d"%friend_user_id
        #username是唯一的,要不没有数据,要不只有一条数据
        data_info = self.db_operate.do_sql(sql,flag)
        if data_info[0][0] == '1':
            friend_addr = (data_info[0][1],data_info[0][2])
            print('地址信息',friend_addr)
            send_msg = '0651 ' + str(user_id) + ' ' + str(friend_user_id) + ' ' + file_name+ ' OK'
            self.sockfd.sendto(send_msg.encode(),friend_addr)
            print('发送0651成功')
        # 在线就发，不在线情况暂时不做处理
        else:
            print('不在线')

    def video_chat_request(self):
        data_list = self.data.split(' ')
        print("data_list:",data_list)
        user_id = data_list[1]
        friend_user_id = data_list[2]
        video_chat_server_addr = data_list[3]
        video_chat_server_port = data_list[4]
        #查找该用户是否存在
        flag = 0
        sql = "select user_stat,user_ip,user_udp_port from user_tbl where user_id = %d"%int(friend_user_id)
        #username是唯一的,要不没有数据,要不只有一条数据
        data_info = self.db_operate.do_sql(sql,flag)
        print("data_info:",data_info)
        if data_info[0][0] == '1':
            friend_addr = (data_info[0][1],data_info[0][2])
            print('地址信息',friend_addr)
            send_msg = '067 ' + user_id + ' ' + friend_user_id + ' ' + video_chat_server_addr + ' ' + video_chat_server_port
            self.sockfd.sendto(send_msg.encode(),friend_addr)
            print('视频请求转发给C2')
        # 在线就发，不在线情况暂时不做处理
        else:
            print('不在线')

    def promise_vchat(self):
        data_list = self.data.split(' ')
        user_id = data_list[1]
        friend_user_id = data_list[2]
        video_chat_server_addr = data_list[3]
        video_chat_server_port = data_list[4]
        #查找该用户是否存在
        flag = 0
        sql = "select user_stat,user_ip,user_udp_port from user_tbl where user_id = %d"%int(user_id)
        #username是唯一的,要不没有数据,要不只有一条数据
        data_info = self.db_operate.do_sql(sql,flag)
        print("data_info:",data_info)
        if data_info[0][0] == '1':
            user_addr = (data_info[0][1],data_info[0][2])
            print('地址信息',user_addr)
            send_msg = '0671 ' + user_id + ' ' + friend_user_id + ' ' + video_chat_server_addr + ' ' + video_chat_server_port
            self.sockfd.sendto(send_msg.encode(),user_addr)
            print('同意消息转发给C1')
        # 在线就发，不在线情况暂时不做处理
        else:
            print('不在线')

    def interupt_vchat(self):
        data_list = self.data.split(' ')
        user_id = data_list[1]
        friend_user_id = data_list[2]
        mode = data_list[3]
        #查找该用户是否存在
        flag = 0
        sql = "select user_stat,user_ip,user_udp_port from user_tbl where user_id = %d"%int(friend_user_id)
        #username是唯一的,要不没有数据,要不只有一条数据
        data_info = self.db_operate.do_sql(sql,flag)
        print("data_info:",data_info)
        if data_info[0][0] == '1':
            friend_user_addr = (data_info[0][1],data_info[0][2])
            send_msg = '0672 ' + user_id + ' ' + friend_user_id + ' ' + mode
            self.sockfd.sendto(send_msg.encode(),friend_user_addr)
        # 在线就发，不在线情况暂时不做处理
        else:
            print('不在线')

    def voice_chat_request(self):
        data_list = self.data.split(' ')
        print("data_list:",data_list)
        user_id = data_list[1]
        friend_user_id = data_list[2]
        voice_chat_server_addr = data_list[3]
        voice_chat_server_port = data_list[4]
        #查找该用户是否存在
        flag = 0
        sql = "select user_stat,user_ip,user_udp_port from user_tbl where user_id = %d"%int(friend_user_id)
        #username是唯一的,要不没有数据,要不只有一条数据
        data_info = self.db_operate.do_sql(sql,flag)
        print("data_info:",data_info)
        if data_info[0][0] == '1':
            friend_addr = (data_info[0][1],data_info[0][2])
            print('地址信息',friend_addr)
            send_msg = '066 ' + user_id + ' ' + friend_user_id + ' ' + voice_chat_server_addr + ' ' + voice_chat_server_port
            self.sockfd.sendto(send_msg.encode(),friend_addr)
            print('语音请求转发给C2')
        # 在线就发，不在线情况暂时不做处理
        else:
            print('不在线')

    def promise_achat(self):
        data_list = self.data.split(' ')
        user_id = data_list[1]
        friend_user_id = data_list[2]
        voice_chat_server_addr = data_list[3]
        voice_chat_server_port = data_list[4]
        #查找该用户是否存在
        flag = 0
        sql = "select user_stat,user_ip,user_udp_port from user_tbl where user_id = %d"%int(user_id)
        #username是唯一的,要不没有数据,要不只有一条数据
        data_info = self.db_operate.do_sql(sql,flag)
        print("data_info:",data_info)
        if data_info[0][0] == '1':
            user_addr = (data_info[0][1],data_info[0][2])
            print('地址信息',user_addr)
            send_msg = '0661 ' + user_id + ' ' + friend_user_id + ' ' + voice_chat_server_addr + ' ' + voice_chat_server_port
            self.sockfd.sendto(send_msg.encode(),user_addr)
            print('同意消息转发给C1')
        # 在线就发，不在线情况暂时不做处理
        else:
            print('不在线')

    def interupt_achat(self):
        data_list = self.data.split(' ')
        user_id = data_list[1]
        friend_user_id = data_list[2]
        mode = data_list[3]
        #查找该用户是否存在
        flag = 0
        sql = "select user_stat,user_ip,user_udp_port from user_tbl where user_id = %d"%int(friend_user_id)
        #username是唯一的,要不没有数据,要不只有一条数据
        data_info = self.db_operate.do_sql(sql,flag)
        print("data_info:",data_info)
        if data_info[0][0] == '1':
            friend_user_addr = (data_info[0][1],data_info[0][2])
            send_msg = '0662 ' + user_id + ' ' + friend_user_id + ' ' + mode
            self.sockfd.sendto(send_msg.encode(),friend_user_addr)
        # 在线就发，不在线情况暂时不做处理
        else:
            print('不在线')

    def modify_passwd(self):
         #修改密码密码 041+本人ID +newpassword+ oldpassword
        data_list = self.data.split(' ')
        print(data_list)
        length = len(data_list)
        if length < 4:
            self.sockfd.sendto(b'041 Failed',self.addr)
            return
        user_id = int(self.data.split(' ')[1])
        new_passwd = self.data.split(' ')[3]
        old_passwd = self.data.split(' ')[2]
        if new_passwd == old_passwd:
            self.sockfd.sendto(b'041 Failed',self.addr)
            return
        #查询用户名和密码是否匹配 查询返回的data是元组 或者None
        flag = 0
        sql =  "select * from user_tbl where user_id= %d and passwd = '%s'"%(user_id,old_passwd)
        data = self.db_operate.do_sql(sql,flag)
        if not data:
            print("密码不一致")
            self.sockfd.sendto(b'041 Failed',self.addr)
        else:
            flag = 1
            sql =  "update user_tbl set passwd = '%s' where user_id = '%s'"%(new_passwd,user_id)
            update_data = self.db_operate.do_sql(sql,flag)
            if not update_data:
                print("修改密码失败...")
                self.sockfd.sendto(b'041 Failed',self.addr)
            else:
                print("修改密码成功...")
                self.sockfd.sendto(b'041 OK',self.addr)
        return

    def modify_tel_no(self):
        #042+user_id + newtelno
        data_list = self.data.split(' ')
        length = len(data_list)
        if length < 3 :
            self.sockfd.sendto(b'042 Failed',self.addr)
            return
        user_id = int(self.data.split(' ')[1])
        new_user_tel = self.data.split(' ')[2]
        #查询用户名和密码是否匹配 查询返回的data是元组 或者None
        flag = 0
        sql =  "select * from user_tbl where user_tel ='%s'"%(new_user_tel)
        data = self.db_operate.do_sql(sql,flag)
        if data:
            self.sockfd.sendto(b'042 Failed',self.addr)
        else:
            flag = 1
            sql =  "update user_tbl set user_tel = '%s' where user_id = %d"%(new_user_tel,user_id)
            update_data = self.db_operate.do_sql(sql,flag)
            if not update_data:
                print("修改电话号码失败...")
                self.sockfd.sendto(b'042 Failed',self.addr)
            else:
                print("修改电话号码成功...")
                self.sockfd.sendto(b'042 OK',self.addr)
        return

    def modify_gender(self):
        #043 + user_id + gender
        data_list = self.data.split(' ')
        length = len(data_list)
        if length < 3 :
            self.sockfd.sendto(b'043 Failed',self.addr)
            return
        user_id = int(self.data.split(' ')[1])
        gender = self.data.split(' ')[2]
        # if gender =='0' or gender =='1':
        #     gender = int(gender)   
        #查询用户名和密码是否匹配 查询返回的data是元组 或者None
        flag = 0
        sql =  "select * from user_tbl where user_id ='%s'"%(user_id)
        data = self.db_operate.do_sql(sql,flag)
        if not data:
            self.sockfd.sendto(b'043 Failed',self.addr)
            return
        else:
            flag = 1
            sql =  "update user_tbl set gender = '%s' where user_id = %d"%(gender,user_id)
            update_data = self.db_operate.do_sql(sql,flag)
            if not update_data:
                print("修改性别失败...")
                self.sockfd.sendto(b'043 Failed',self.addr)
            else:
                print("修改性别成功...")
                self.sockfd.sendto(b'043 OK',self.addr)
        return

    def modify_birthdate(self):
        #044 +本人ID + birthdate
        data_list = self.data.split(' ')
        length = len(data_list)
        if length < 3 :
            self.sockfd.sendto(b'043 Failed',self.addr)
            return
        user_id = int(self.data.split(' ')[1])
        brith = self.data.split(' ')[2]
        #将字符串转换为日期类型
        # brith = datetime.datetime.strptime(birthdate,'%Y-%m-%d').date()
        #查询用户名和密码是否匹配 查询返回的data是元组 或者None
        flag = 0
        sql =  "select * from user_tbl where user_id ='%s'"%(user_id)
        data = self.db_operate.do_sql(sql,flag)
        if not data:
            self.sockfd.sendto(b'044 Failed',self.addr)
        else:
            flag = 1
            sql =  "update user_tbl set brith = '%s' where user_id = %d"%(brith,user_id)
            update_data = self.db_operate.do_sql(sql,flag)
            if not update_data:
                print("修改出生日期失败...")
                self.sockfd.sendto(b'044 Failed',self.addr)
            else:
                print("修改出日期成功...")
                self.sockfd.sendto(b'044 OK',self.addr)
        return

    def message_free(self):
        pass

    def keep_alive(self,queue_online):
        #首先从队列取在线字典 000 user_id alive 更新时间{user_name time}
        data_list = self.data.split(' ')
        user_id = int(data_list[1])
        online_dict = queue_online.get()
        print(online_dict.keys())
        #更新字典
        print("有人发心跳包过来",user_id)
        if user_id in online_dict:
            print("客户端发来报活信息。。。",user_id)
            online_dict[user_id] = time.time()
            queue_online.put(online_dict)
            #更新数据库
        else:
            print("客户端上线。。。",user_id)
            online_dict[user_id] = time.time()
            queue_online.put(online_dict)

    def ack_pack(self):
        pass

