#!/usr/bin/env python

def stop_iteration_001():
    """
    StopIteration 异常示例
    :return:
    """
    gennumber = (i for i in range(1, 2))
    print(next(gennumber))
    print(next(gennumber))
    try:
        print(next(gennumber))
    except StopIteration as e:
        print("最后一个元素")


class UserInputError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self, ErrorInfo)
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


def user_defined_exception_002():
    """
    用户自定义异常
    :return:
    """
    userinput = 'a'
    try:
        if not userinput.isdigit():
            raise UserInputError('用户输入错误')
    except UserInputError as e:
        print(e)
    finally:
        del userinput
