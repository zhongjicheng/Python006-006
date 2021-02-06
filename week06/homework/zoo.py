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


class Animal(metaclass=ABCMeta):
    def __init__(self, animal_type, size, character):
        self.animal_type = animal_type
        self.size = size  # 体型（小，中等，大型）
        self.character = character

    @property
    def is_ferocious_animals(self):
        if self.size != "小" and self.animal_type == "食肉" and self.character == "凶猛":
            return True
        return False

    @abstractmethod
    def is_pet(self):
        pass


class Cat(Animal):
    sounds = "mew"

    def __init__(self, cat_name, animal_type, size, character):
        super(Cat, self).__init__(animal_type, size, character)
        self.cat_name = cat_name

    @property
    def is_pet(self):
        return not self.is_ferocious_animals

    @classmethod
    def get_sounds(cls):
        return cls.sounds


class Dog(Animal):
    sounds = "woof"

    def __init__(self, cat_name, animal_type, size, character):
        super(Dog, self).__init__(animal_type, size, character)
        self.cat_name = cat_name

    @property
    def is_pet(self):
        return not self.is_ferocious_animals

    @classmethod
    def get_sounds(cls):
        return cls.sounds


class Zoo(object):
    animal_instance_dic = []

    def __init__(self, zoo_name):
        self.zoo_name = zoo_name

    @classmethod
    def add_animal(cls, animal: Animal):
        """
        添加动物到动物园
        :param animal: Animal 实例
        :return:
        """
        if cls.animal_instance_dic:
            for animal in cls.animal_instance_dic:
                if type(animal) is type(animal):
                    return cls.animal_instance_dic
            else:
                cls.animal_instance_dic.append(animal)
        else:
            cls.animal_instance_dic.append(animal)

    @classmethod
    def print_animals(cls):
        print(cls.animal_instance_dic)


def hasattr(zoo: Zoo, animal: Animal):
    """
    动物园是否有 ‘animal’ 这种动物
    :param zoo: Zoo 实例
    :param animal: Animal 实例
    :return:
    """
    if zoo.animal_instance_dic:
        for animal_instance in zoo.animal_instance_dic:
            if type(animal_instance) is type(animal):
                return True
        else:
            return False
    else:
        return False


if __name__ == "__main__":
    dog = Dog('藏獒', '食肉', '大型', '凶猛')
    cat = Cat('大花猫 1', '食肉', '小', '温顺')
    print(cat.is_ferocious_animals)
    print(cat.get_sounds())
    print(cat.is_pet)
    z = Zoo('时间动物园')
    z.add_animal(cat)
    z.add_animal(dog)
    z.print_animals()
    print(hasattr(z, cat))
    print(hasattr(z, dog))
