from socket import *
from multiprocessing import Process

HOST = '127.0.0.1'
PORT = 8081
ADDR = (HOST,PORT)
sockfd = socket(AF_INET,SOCK_DGRAM)
def recv_data(sockfd):
    while True:
        data,addr = sockfd.recvfrom(1024)
        print(data.decode())
p = Process(target = recv_data,args = (sockfd,))
p.daemon = True
p.start()
while True:
    send_data = input("输入命令:")
    if not send_data:
        break
    sockfd.sendto(send_data.encode(),ADDR)