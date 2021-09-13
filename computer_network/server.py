# -*- encoding=utf-8 -*-

import socket
from operate_system.pool import ThreadPool as tp
from operate_system.task import AsyncTask
import json

from parser import IPParser

class ProcessTask(AsyncTask):
    def __init__(self, packet, *args, **kwargs) -> None:
        super().__init__(func=self.process, *args, **kwargs)
        self.packet = packet

    def process(self):
        ip_header = IPParser.parse(self.packet)
        return ip_header

class Server:
    def __init__(self) -> None:
        # 工作协议类型，套接字类型，工作具体协议
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, 
                                socket.IPPROTO_IP)
        # 绑定自己的主机IP
        self.ip = "192.168.1.13"
        self.port = 8888
        self.sock.bind((self.ip,self.port))

        # 设置混杂模式，开启混杂模式
        self.sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        # 新建一个线程池
        self.pool = tp(10)
           
    def loop_server(self):
        while True:
            # 接收
            packet, addr = self.sock.recv(65535)
            # 生成task
            task = ProcessTask(packet)
            # 提交任务
            self.pool.put(task)
            # 获取结果
            result = task.get_result()
            result = json.dumps(
                result,
                indent=4
            )

if __name__ == "__main__":
    server = Server()
    server.loop_server()