#!/usr/bin/env python
import socket

HOST = 'localhost'
PORT = 10000


def echo_client():
    '''
    Echo server 的 Client 端
    :return:
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    with open('a.jpg', 'rb') as f:
        data = f.read()
        # 发送数据到服务端
        s.sendall(data)
    s.close()


if __name__ == "__main__":
    echo_client()
