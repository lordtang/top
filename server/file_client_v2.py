# 客户端
import socket
import os,sys
import hashlib
def handle():
    client = socket.socket()  # 生成socket连接对象
    client.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    ip_port =("localhost", 6969)  # 地址和端口号
    client.connect(ip_port)  # 连接

    print("成功连接服务器")

    while True:
        content = input(">>")

        if len(content)==0: continue  # 如果传入空字符会阻塞
        #客户端接收服务器文件
        if content.startswith("get"):
            file_name = content.split(' ')[1]
            file_info = 'get'+ ' ' + file_name +' '+ '0'
            client.send(file_info.encode("utf-8"))  # 传送和接收都是bytes类 型
            # 1.先接收文件长度，建议8192
            server_response = client.recv(1024)
            if server_response.decode('utf-8').split(' ')[0] == 'F':
                sys.exit('not found')
            else:
                file_size = int(server_response.decode("utf-8"))

                print("接收到的大小：", file_size)

                # 2.接收文件内容
                client.send("准备好接收".encode("utf-8"))  # 接收确认
                filename = "new" + content.split(" ")[1]

                f = open(filename, "wb")
                received_size = 0
                m = hashlib.md5()

                while received_size < file_size:
                    size = 0  # 准确接收数据大小，解决粘包
                    if file_size - received_size > 1024: # 多次接收
                        size = 1024
                    else:  # 最后一次接收完毕
                        size = file_size - received_size

                    data = client.recv(size)  # 多次接收内容，接收大数据
                    data_len = len(data)
                    received_size += data_len
                    print("已接收：", int(received_size/file_size*100),     "%")

                    m.update(data)
                    f.write(data)

                f.close()

                print("实际接收的大小:", received_size)  # 解码

                # 3.md5值校验
                md5_sever = client.recv(1024).decode("utf-8")
                md5_client = m.hexdigest()
                print("服务器发来的md5:", md5_sever)
                print("接收文件的md5:", md5_client)
                if md5_sever == md5_client:
                    print("MD5值校验成功")
                    # print('获取成功')
                    sys.exit('获取成功')
                else:
                    print("MD5值校验失败")
        # 客户端向服务器发送文件
        elif content.startswith("put"):
            filename = content.split(' ')[1]
            if os.path.isfile(filename):  # 判断文件存在
                # 1.先发送文件大小，让服务端准备接收
                size = os.stat(filename).st_size  #获取文件大小
                file_info = 'put' +' '+ filename+' '+str(size)
                client.send(file_info.encode("utf-8"))  # 发送数度
                print("发送的大小：", size)
                # 2.发送文件内容
                client.recv(1024)  # 接收确认
                m = hashlib.md5()
                f = open(filename, "rb")
                for line in f:
                    client.send(line)  # 发送数据
                    m.update(line)
                f.close()
                # 3.发送md5值进行校验
                md5 = m.hexdigest()
                client.send(md5.encode("utf-8"))  # 发送md5值
                print("md5:", md5)
                data = client.recv(1024).decode()
                print(data)
                sys.exit()
                # os._exit(1)
            #文件不存在
            else:
                sys.exit('文件不存在，请重新输入')
        else:
            print('''
            for example>>get test.txt
                       >>put text.txt
            ''')
            sys.exit()



    client.close()

    
if __name__ == "__main__":
    handle()