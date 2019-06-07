from PIL import Image
from io import BytesIO
from socket import *
path = '/home/tarena/test/middle_work/'
def pic_client():
    client = socket()
    client.connect(('localhost',6969))
    filename = 'color.jpg'
    file_path = path + filename
    while True:
        cmd = input("输入你的命令")
        if cmd == "get_pic":
            send_msg = cmd + " " + filename
            client.send(send_msg.encode())
            img_data = b""
            while True:
                data = client.recv(1024)
                img_data += data
                if data == b'##':
                    break
            buf = BytesIO(img_data)
            img_obj =Image.open(buf)
            #图片格式的后缀名判断
            suffix = file_name.split('.')[-1]
            img_obj.save(file_path,format(suffix))
        elif cmd == "put_pic":
            send_msg = cmd + " " + filename
            client.send(send_msg.encode())
            f = open(file_path,'rb')
            while True:
                data = f.read(1024)
                if not data:
                    sleep(1)
                    client.send(b"##")
                    break
                client.send(data)
        #传输完成后就退出
        break
        #解决粘包
    client.close()

pic_client()