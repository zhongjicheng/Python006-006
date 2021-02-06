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
    feeding_habits = ('素食', '杂食', '肉食')
    sizes = ('小型', '中等', '大型')
    characters = ('温顺', '中性', '凶猛')

    def __init__(self, feeding_habit, size, character):
        if feeding_habit not in Animal.feeding_habits:
            raise ValueError(f'Only {Animal.feeding_habits} can be selected')
        if size not in Animal.sizes:
            raise ValueError(f'Only {Animal.sizes} can be selected')
        if character not in Animal.characters:
            raise ValueError(f'Only {Animal.characters} can be selected')
        self.feeding_habit = feeding_habit
        self.size = size
        self.character = character

    @property
    def is_ferocious(self):
        if self.size != Animal.sizes[0] and self.feeding_habit == Animal.feeding_habits[2] and self.character == \
                Animal.characters[2]:
            return True
        return False

    @abstractmethod
    def is_pet_able(self):
        pass


class Cat(Animal):
    sounds = "meow"

    def __init__(self, name, feeding_habit, size, character):
        super(Cat, self).__init__(feeding_habit, size, character)
        self.name = name

    @property
    def is_pet_able(self):
        return not self.is_ferocious

    @classmethod
    def get_sounds(cls):
        return cls.sounds

    def __repr__(self):
        print(f'Cat: {self.name}')


class Dog(Animal):
    sounds = "woof"

    def __init__(self, name, feeding_habit, size, character):
        super(Dog, self).__init__(feeding_habit, size, character)
        self.name = name

    @property
    def is_pet_able(self):
        return not self.is_ferocious

    @classmethod
    def get_sounds(cls):
        return cls.sounds

    def __repr__(self):
        print(f'Dog: {self.name}')


class Zoo(object):
    animals = []

    def __init__(self, name):
        self.name = name

    @classmethod
    def add_animal(cls, animal: Animal):
        """
        添加动物到动物园
        :param animal: Animal 实例
        :return:
        """
        if cls.animals:
            for animal_instance in cls.animals:
                if type(animal) == type(animal_instance):
                    break
            else:
                cls.animals.append(animal)
        else:
            cls.animals.append(animal)

    def __repr__(self):
        print(f'Zoo: {self.name}')


def hasattr(zoo: Zoo, animal: Animal):
    """
    动物园是否有 ‘animal’ 这种动物
    :param zoo: Zoo 实例
    :param animal: Animal 实例
    :return:
    """
    if zoo.animals:
        for animal_instance in zoo.animals:
            if animal.name == animal_instance.name:
                return True
        else:
            return False
    else:
        return False


if __name__ == "__main__":
    # 初始化3只动物到动物类
    dog = Dog('藏獒', '肉食', '大型', '凶猛')
    dog_jinmao = Dog('金毛', '肉食', '中等', '温顺')
    cat = Cat('大花猫', '肉食', '小型', '温顺')

    # 打印各动物的属性
    print(f"{cat.name} is ferocious: {cat.is_ferocious}")
    print(f"Sound of {cat.name} is: {cat.get_sounds()}")
    print(f"{cat.name} is pet able: {cat.is_pet_able}")
    print(f"{dog.name} is ferocious: {dog.is_ferocious}")
    print(f"Sound of {dog.name} is: {dog.get_sounds()}")
    print(f"{dog.name} is pet able: {dog.is_pet_able}")

    # 添加动物到动物园
    z = Zoo('时间动物园')
    z.add_animal(cat)
    z.add_animal(cat)
    z.add_animal(dog)
    z.add_animal(dog)

    # 检查动物园是否有已初始化的动物
    print(f"{z.name} has {cat.name}: {hasattr(z, cat)}")
    print(f"{z.name} has {dog.name}: {hasattr(z, dog)}")
    print(f"{z.name} has {dog_jinmao.name}: {hasattr(z, dog_jinmao)}")
