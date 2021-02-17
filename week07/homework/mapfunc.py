"""
作业二：
自定义一个 python 函数，实现 map() 函数的功能。
"""

from record_log import RecordLog


def mymap(func, *iterables):
    """
    实现map功能
    :param func:
    :param iterables:
    :return:
    """
    log = RecordLog().logger
    args_len = len(iterables)
    single_arg_len = len(iterables[0])
    log.info(f"args_len:{args_len}")
    log.info(f"single_arg_len:{single_arg_len}")
    for it in iterables:
        # 判断参数是否为可迭代对象
        if not hasattr(it, "__iter__"):
            raise ValueError(f"object[{it}] has not __iter__ func")
        # 判断各参数的长度是否一致
        if len(it) != single_arg_len:
            raise ValueError(f"Length of {it} not equal to {single_arg_len}")

    # 把所有可迭代的对象按index位置按tuple数据类型存入func_input_args
    func_input_args = []
    for i in range(single_arg_len):
        tmp_list = []
        for arg in iterables:
            tmp_list.append(arg[i])
        func_input_args.append(tuple(tmp_list))
    log.info(func_input_args)

    # 执行函数
    for arg in func_input_args:
        yield func(*arg)


def add(x):
    return x + 1


def add1(x, y, z):
    return x + y + z


if __name__ == "__main__":
    l = [1, 2, 3]
    l1 = (4, 5, 6,)
    l3 = [7, 8, 9]

    # 参数检查验证
    # mymap(add1, l, [1, 2])
    # mymap(add1, l, 3)

    # 单个可迭代参数验证
    m = mymap(add, l)
    print(list(m))
    # print(next(m))

    # 多个可迭代参数传入验证
    m = mymap(add1, l, l1, l3)
    print(f"list of m:{list(m)}")
