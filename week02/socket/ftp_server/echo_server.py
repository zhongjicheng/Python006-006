#!/usr/bin/env python
import socket
import threading

HOST = 'localhost'
PORT = 10000
NUM_CLIENT = 100


def save_file(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        with open("./a.jpg", 'ab') as f:
            f.write(data.decode('utf-8'))
    conn.close()


def echo_server():
    '''
    Echo Server 的 Server 端
    :return:
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 对象s绑定到指定对主机和端口上
    s.bind((HOST, PORT))
    # 只接受1个链接
    s.listen(NUM_CLIENT)
    while True:
        # accept 表示接受用户端对链接
        conn, addr = s.accept()
        # 输出客户端地址
        print(f'Conneted by {addr}')

        # 创建线程执行echo信息任务
        th1 = threading.Thread(target=save_file, args=(conn,))
        th1.start()


if __name__ == '__main__':
    echo_server()
