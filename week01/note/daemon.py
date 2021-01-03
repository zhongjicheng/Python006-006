# ！/usr/bin/env python
import sys
import os
import time

'''
手动写一个daemon进程
'''


def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    try:
        # 创建子进程
        pid = os.fork()

        if pid > 0:
            # 父进程先于子进程exit，会使子进程变为孤儿进程，
            # 这样子进程成功被init这个用户级守护进程收养
            sys.exit(0)

    except OSError as err:
        sys.stderr.write('_Fork #1 failed: {0}\n'.format(err))
        sys.exit(1)

    # 从父进程环境脱离
    # decouple from parent environment
    # chdir确认进程不占用任何目录，否则不能umount
    os.chdir("/")
    # 调用umask(0)拥有写任何文件对权限，避免继承自父进程对umask被修改导致自身权限不足
    os.umask(0)
    # setsid调用成功后，进程成为新对会话组长和新的进程组长，并与原来对登录会话和进程组脱离
    os.setsid()

    # 第二次fork,再次fork对子进程作为守护进程继续运行
    # 保证了该守护进程不再是会话对首进程
    # 只有会话首进程才可以打开终端设备，daemon进程对目的就是不打开控制终端
    # fork两次可以避免后期进程误操作而再次打开终端tty设备
    try:
        pid = os.fork()
        if pid > 0:
            # 第二个父进程退出
            sys.exit(0)
    except OSError as err:
        sys.stderr.write('_Fork #2 failed: {0}\n'.format(err))
        sys.exit(1)

    # 重定向标准文件描述符
    sys.stdout.flush()
    sys.stderr.flush()

    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'w')

    # dup2函数原子化关闭和复制文件描述符
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


def test():
    sys.stdout.write('Daemon started with pid %d\n' % os.getpid())
    while True:
        now = time.strftime("%X", time.localtime())
        sys.stdout.write(f'{time.ctime()}\n')
        sys.stdout.flush()
        time.sleep(1)


if __name__ == "__main__":
    daemonize('/dev/null', '//home/zjc/workspace/week1/d1.log', '/dev/null')
    test()
