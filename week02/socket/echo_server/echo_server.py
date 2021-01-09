#!/usr/bin/env python
import socket

HOST = 'localhost'
PORT = 10000


def echo_server():
    '''
    Echo Server 的 Server 端
    :return:
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 对象s绑定到指定对主机和端口上
    s.bind((HOST, PORT))
    # 只接受1个链接
    s.listen(1)
    while True:
        # accept 表示接受用户端对链接
        conn, addr = s.accept()
        # 输出客户端地址
        print(f'Conneted by {addr}')
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
        conn.close()


if __name__ == '__main__':
    echo_server()
