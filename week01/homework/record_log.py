#!/usr/bin/env python

'''
编写一个函数, 当函数被调用时，将调用的时间记录在日志中, 日志文件的保存位置建议为：/var/log/python- 当前日期 /xxxx.log
'''

import time
import logging
from pathlib import Path


def make_log_path():
    """
    创建日志目录：/var/log/python-当前日期
    :return: 日志目录
    """
    local_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    log_path = f"/var/log/python-{local_time}"
    log_p = Path(log_path)
    log_p.mkdir(parents=True, exist_ok=True)

    return log_path


def record_log():
    """
    日志记录
    :return:
    """
    log_path = make_log_path()
    logging.basicConfig(filename=f"{log_path}/test.log", level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S",
                        format='%(asctime)s %(name)-8s %(levelname)-8s [%(filename)s:%(funcName)s :%(lineno)d] %(message)s')
    logging.debug('debug')
    logging.info('info')
    logging.warning('warning')
    logging.error('error')
    logging.critical('critical')


if __name__ == "__main__":
    record_log()
