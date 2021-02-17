"""
作业二：
自定义一个 python 类，实现 map() 函数的功能。
"""

from collections.abc import Iterator, Iterable
from record_log import RecordLog


class MapClass(object):
    """
    map(func, *iterables) --> map object

    Make an iterator that computes the function using arguments from
    each of the iterables.  Stops when the shortest iterable is exhausted.
    """

    def __init__(self, func, *iterables):  # real signature unknown; restored from __doc__
        self.log = RecordLog().logger
        self.func = func
        self.index = 0
        args_len = len(iterables)
        single_arg_len = len(iterables[0])
        self.log.info(f"args_len:{args_len}")
        self.log.info(f"single_arg_len:{single_arg_len}")
        for it in iterables:
            # 判断参数是否为可迭代对象
            if not hasattr(it, "__iter__"):
                raise ValueError(f"object[{it}] has not __iter__ func")
            # 判断各参数的长度是否一致
            if len(it) != single_arg_len:
                raise ValueError(f"Length of {it} not equal to {single_arg_len}")
        # 把所有可迭代的对象按index位置按tuple数据类型存入func_input_args
        self.func_input_args = []
        for i in range(single_arg_len):
            tmp_list = []
            for arg in iterables:
                tmp_list.append(arg[i])
            self.func_input_args.append(tuple(tmp_list))
        self.log.info(self.func_input_args)

    def __iter__(self, *args, **kwargs):  # real signature unknown
        """ Implement iter(self). """
        return MyInterator(self.func, self.func_input_args)

    def __next__(self, *args, **kwargs):  # real signature unknown
        """ Implement next(self). """
        try:
            ret = self.func(*self.func_input_args[self.index])
        except IndexError:
            raise StopIteration
        self.index += 1
        return ret


class MyInterator(Iterator):
    def __init__(self, func, func_input_args):
        self.index = 0
        self.func = func
        self.func_input_args = func_input_args

    def __next__(self):
        try:
            ret = self.func(*self.func_input_args[self.index])
        except IndexError:
            raise StopIteration
        self.index += 1
        return ret


def add(x):
    return x + 1


def add1(x, y, z):
    return x + y + z


if __name__ == "__main__":
    l = [1, 2, 3]
    l1 = (4, 5, 6,)
    l3 = [7, 8, 9]

    # 参数检查验证
    # MapClass(add1, l, [1, 2])
    # MapClass(add1, l, 3)

    # 可迭代验证
    a = MapClass(add, l)
    for i in a:
        print(i)

    # 多个可迭代参数传入验证
    m = MapClass(add1, l, l1, l3)
    print(f"list of m:{list(m)}")
    print(next(m))
    print(next(m))
    print(next(m))
