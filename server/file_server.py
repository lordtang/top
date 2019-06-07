# 服务器
from log import *
from  socket import *
import os,sys
import hashlib
from multiprocessing import Pool,Process

path = '/home/ayuan/Top/file_store'


def file_server():
    server = socket()
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 6969))  # 绑定监听端口
    server.listen(5)  # 监听
    logger.info("文件服务器正在监听..")
    pool = Pool(8)

    while True:
        try:
            conn,addr = server.accept()  # 等待连接
        except Exception as e:
            logger.info('Error:{}'.format(e))
            continue

        logger.info("conn:{}\naddr:{}".format(conn, addr))  # conn连接实例
        pool.apply_async(func = handle,args = (conn,))

    server.close()
    pool.close()
    pool.join()


def handle(conn):
    while True:
        try:
            data = conn.recv(1024)  # 接收
        except Exception as e:
            logger.info('Error:{}'.format(e))
        if not data:  # 客户端已断开
            logger.info("客户端断开连接\r\n")
            break
        logger.info("收到的命令：{}".format(data.decode("utf-8")))
        cmd = data.decode("utf-8").split("*^$*#%*")[0]
        file_name = data.decode("utf-8").split("*^$*#%*")[1]
        file_size = int(data.decode("utf-8").split("*^$*#%*")[2])
        # 客户端下载服务器文件
        if cmd == "get":
            print("客户端接收文件")
            file_path = 'temp_transend_files/' + file_name
            if os.path.exists(file_path):  # 判断文件存在
                logger.info("成功找到文件：{}".format(file_path))
                # 1.先发送文件大小，让客户端准备接收
                size = os.stat(file_path).st_size  # 获取文件大小
                conn.send(str(size).encode("utf-8"))  # 发送文件小
                logger.info("发送的大小：{}".format(size))
                # 2.发送文件内容
                conn.recv(1024)  # 接收确认
                m = hashlib.md5()
                f = open(file_path, "rb")
                for line in f:
                    conn.send(line)  # 发送数据
                    m.update(line)
                f.close()
                os.remove(file_path) #发送图片完毕删除图片
                # 3.发送md5值进行校验
                md5 = m.hexdigest()
                conn.send(md5.encode("utf-8"))  # 发送md5值
                logger.info('md5:{}'.format(md5))
            else:
                conn.send('F not found'.encode())
                logger.info('没找到文件')
        # 客户端上传文件到服务器
        elif cmd == "put":
            # 接收文件内容
            conn.send("准备好接收".encode("utf-8"))
            path = 'temp_transend_files/'+file_name
            f = open(path, "wb")
            received_size = 0
            m = hashlib.md5()
            while received_size < int(file_size):
                size = 0  # 准确接收数据大小，解决粘包
                if file_size - received_size > 1024:  # 多次接收
                    size = 1024
                else:  # 最后一次接收完毕
                    size = file_size - received_size
                data = conn.recv(size)  # 多次接收内容，接收大文件
                if not data:
                    print("客户端终止文件传输")
                    f.close()
                    os.remove(path)
                    return
                data_len = len(data)
                received_size += data_len
                logger.info("已接收：{}%".format(
                    int(received_size/file_size*100)))
                m.update(data)
                f.write(data)
            
            f.close()
            logger.info("实际接收的大小:{}".format(received_size)) # 解码
            # md5值校验
            md5_sever = conn.recv(1024).decode("utf-8")
            md5_client = m.hexdigest()
            logger.info("服务器发来的md5:{}".format(md5_sever))
            logger.info("接收文件的md5:{}".format(md5_client))
            if md5_sever == md5_client:
                logger.info("MD5值校验成功")
                conn.send('发送成功'.encode())
            else:
                logger.info("MD5值校验失败")
                conn.send('发送失败，请重新发送'.encode())
    conn.close()



if __name__ == "__main__":
    file_server()
    try:
        file_server()
    except Exception as e:
        logger.info('Error:{}'.format(e))
