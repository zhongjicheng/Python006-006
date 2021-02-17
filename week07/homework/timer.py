"""
作业三：
实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。
"""

import time
from functools import wraps


def timer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        star_time = time.time()
        time.sleep(3)
        ret = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} cost time:{end_time - star_time}")
        return ret

    return inner


@timer
def foo(*args, **kwargs):
    pass


print(foo(1, 3, 5))
