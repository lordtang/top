import time
#定时任务 传入参数 定时时间 进程通信队列(实现进程之间的通信)
def alive(sec,queue_online):
    check_time = time.time()
    online_dict = queue_online.get()
    for key,last_time in list(online_dict.itmes()):
        limit_time = check_time - last_time
        if limit_time > sec:
            #删除字典 并更新数据库 修改last_time字段和状态字段
            pass
        else:
            #更新字典
            pass
    queue_online.put(online_dict)
        
