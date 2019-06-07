from PIL import Image
from io import BytesIO
from socket import *
from time import sleep
path = '/home/tarena/test/middle_work/new_qq_server/'
def pic_server():
    server = socket()
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(("localhost", 6969))  # 绑定监听端口
    server.listen(5)
    while True:
        conn,addr = server.accept()  # 等待连接
        data = conn.recv(1024)
        cmd = data.decode("utf-8").split(" ")[0]
        file_name = data.decode("utf-8").split(" ")[1]
        file_path = path + file_name
        if cmd == "put_pic":
            data = b""
            while True:
                data += conn.recv(1024)
                if data == b'##':
                    break
            buf = BytesIO(data)
            img_obj =Image.open(buf)
            suffix = file_name.split('.')[-1]
            img_obj.save(file_path,format(suffix))
        elif cmd == "get_pic":
            f = open(file_path,'rb')
            while True:
                data = f.read(1024)
                if not data:
                    sleep(1)
                    conn.send(b'##')
                    break
                conn.send(data)
            print("传输完成...")
            #解决粘包
        conn.close()
pic_server()
        
        