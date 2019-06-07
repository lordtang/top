import time
import pymysql 
from dboper import *
#创建数据库实体类
db_operate =DBOper()
#连接数据库
db_operate.open_conn()
# user_name = 'xiaohan'
# friend_user_name = '10001'
# cmd = '031'
# content = concat('031 ',user_name,' ',friend_user_name)
# print(content)
# content = '%s '%cmd + user_name + ' ' + friend_user_name
# data = ""
# with open("/home/tarena/test/middle_work/xiaohan_new2019/color.jpg",'rb') as f:
#     data = f.read()
#     print(len(data))

# user_name = 'adm'
# passwd = '123456'
# gender = 'f'
# birth = '1991-01-01'
# user_tel = '18388303743'
# ip = '176.209.108.41'
# port = 8080

flag = 1
# sql = "insert into user_tbl(user_id,user_name,passwd,gender,brith,user_tel,user_stat,user_ip, user_tcp_port,last_time) values(10000,'%s','%s','%s','%s','%s','1','%s','%s',now())"%(user_name,passwd,gender,birth,user_tel,ip,port)
# sql = "insert into msg_temp(user_name,dest_user_name,content,send_time) values('%s','%s','%s',now())"%(user_name,friend_user_name,content)
# flag = 0
# user_name = '八月'
# sql =  "select user_id from user_tbl where user_name = '%s'"%(user_name)
# sql_update = "update user_tbl set user_stat = '0' where user_id = 10000"
# sql = "update user_tbl set logo = %s"%pymysql.Binary(data)
# print(sql)
sql = "insert into user_friends(friend_id,owner_id,join_date) values('10004','10001',now())"
data_status = db_operate.do_sql(sql,flag)
if not data_status:
    print("添加好友实体失败。。。")
else:
    print("添加好友实体成功。。。。")
db_operate.close_conn()