import socket

def server():
    # 创建套接字
    s = socket.socket()

    # 绑定套接字
    host = "127.0.0.1"
    port = 6666
    s.bind((host, port))

    # 监听套接字
    s.listen(5)
    
    # 使用套接字
    while True:
        c, addr = s.accept() # c是新的绑定，addr是服务器IP地址
        print("connect address is",addr)
        c.send(b"welcome to my server")
        c.close()

if __name__ == "__main__":
    server()