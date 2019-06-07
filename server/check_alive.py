import time
#定时任务 传入参数 定时时间 进程通信队列(实现进程之间的通信)
def alive(sec,db_oper,q):
    while True:
        print(sec)
        time.sleep(int(sec))
        check_time = time.time()
        print("检查时间",check_time)
        client_dict = q.get()
        if client_dict:
            for user_id,last_time in list(client_dict.items()):
                print("开始检测用户是否离线。。。。")
                if abs(last_time - check_time) > sec:
                    # 删除字典 并更新数据库 修改last_time字段和状态字段
                    del client_dict[user_id]  # 删除断开的客户端
                    print("删除不在线客户端")
                    print(client_dict)
                    flag = 1
                    sql_update = "update user_tbl set user_stat = '0',last_time = now() where user_id = %d"%(user_id)
                    data_status = db_oper.do_sql(sql_update,flag)   
                    print(data_status)
        print(client_dict)
        q.put(client_dict)
       

def get_online_dict(db_oper):
    flag = 0
    sql = "select user_id from user_tbl where user_stat ='1'"
    data_info = db_oper.do_sql(sql,flag)
    online_dict = {}
    if not data_info:
        return online_dict
    else:
        for data in data_info:
            online_dict[data[0]] = time.time()
        return online_dict