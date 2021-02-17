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
