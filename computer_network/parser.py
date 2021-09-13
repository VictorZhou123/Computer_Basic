# -*- encoding=utf-8 -*-

import struct, socket
from typing import Protocol

# IP报文解析器
class IPParser:

    IP_HEADER_LENGTH = 20

    @classmethod
    def parser_ip_header(cls, ip_header):
        '''
        IP 报文格式
        第一行：4位IP-Version 4位IP头长度 8位服务类型 16位总长度
        第二行：16位标识符 3位标记位 3位片偏移
        第三行：8位TTL 8位协议 16位IP头校验和
        第四行：32位源IP地址
        第五行：32位目的IP地址
        '''
        # 解析第一行，1（IP-Version和IP头长度）+1+2=4字节
        line1 = struct.unpack('>BBH', ip_header[:4])
        # eg:00001111右移4位得到高4位
        ip_version = line1[0] >> 4 
        # eg:00001111 & 00001111与运算15，得到低4位
        ip_length = line1[0] & 15
        pkg_length = line1[2]
        # 解析第三行，
        line3 = struct.unpack('>BBH', ip_header[8:12])
        TTL = line3[0]
        protocol = line3[1]
        iph_checksum = line3[2]
        # 解析第四行
        line4 = struct.unpack('>L', ip_header[12:16])
        src_ip = socket.net_ntoa(line4[0])
        # 解析第五行
        line5 = struct.unpack('>L', ip_header[16:20])
        dst_ip = socket.net_ntoa(line5[0])


        return {
            'ip_version': ip_version,
            'ip_length': ip_length,
            'packet_length': pkg_length,
            'TTL': TTL,
            'protocol': protocol,
            'iph_checksum': iph_checksum,
            'src_ip': src_ip,
            'dst_ip': dst_ip,
        }

    @classmethod
    def parse(cls, packet):
        ip_header = packet[0:20]
        return cls.parse_ip_header(ip_header)