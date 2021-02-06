"""
背景：在使用 Python 进行《我是动物饲养员》这个游戏的开发过程中，有一个代码片段要求定义动物园、动物、猫、狗四个类。

这个类可以使用如下形式为动物园增加一只猫：

if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Cat')
具体要求：

定义“动物”、“猫”、“狗”、“动物园”四个类，动物类不允许被实例化。
动物类要求定义“类型”、“体型”、“性格”、“是否属于凶猛动物”四个属性，是否属于凶猛动物的判断标准是：“体型 >= 中等”并且是“食肉类型”同时“性格凶猛”。
猫类要求有“叫声”、“是否适合作为宠物”以及“名字”三个属性，其中“叫声”作为类属性，除凶猛动物外都适合作为宠物，猫类继承自动物类。狗类属性与猫类相同，继承自动物类。
动物园类要求有“名字”属性和“添加动物”的方法，“添加动物”方法要实现同一只动物（同一个动物实例）不能被重复添加的功能。
"""

from abc import ABCMeta, abstractmethod
from compare import Rel


class Animal(metaclass=ABCMeta):
    def __init__(self, animal_type, size, character):
        self.animal_type = animal_type
        # 50以下为小型动物，50 以上为大型动物， 50位中型动物
        if self.check_number_range(size, 1, 100, Rel.INC_RIGHT):
            self.size = size
        self.character = character

    def check_number_range(self, arg_value, lower_limit, upper_limit, rel):
        """
        Method for checking whether an int value is in some range.

        Usage:
        - number = check_number_range(number, 0.0, 1.0, Rel.INC_NEITHER, "number", float) # number in [0.0, 1.0]
        - number = check_number_range(number, 0, 1, Rel.INC_NEITHER, "number", int) # number in [0, 1]
        """
        rel_fn = Rel.get_fns(rel)
        if not rel_fn(arg_value, lower_limit, upper_limit):
            rel_str = Rel.get_strs(rel).format(lower_limit, upper_limit)
            raise ValueError("should be in range of {}, but got {} with type `{}`.".format(
                rel_str, arg_value, type(arg_value).__name__))
        return True

    # @abstractmethod
    def is_ferocious_animals(self, arg_value, value, rel):
        ge_fn = Rel.get_fns(Rel.GE)
        eq_fn = Rel.get_fns(Rel.EQ)


a = Animal(1, 101, 3)
