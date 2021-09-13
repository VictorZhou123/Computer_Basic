import socket

def client(i):
    # 创建套接字
    s = socket.socket()
    # 连接套接字
    s.connect(("127.0.0.1",6666))
    # 接收/发送信息
    print('Recv msg: %s, Client: %d' %(s.recv(1024), i)) # 指定接收的长度1024
    s.close()

if __name__ == "__main__":
    for i in range(10):
        client(i)