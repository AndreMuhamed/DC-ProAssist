import itertools

class Person:
    ID = itertools.count()  # Создаем итератор для уникальных ID

    def __init__(self, name, parent=None, level=0):
        self.id = next(self.__class__.ID)  # Получаем уникальный ID
        self.parent = parent  # Родитель текущего узла
        self.name = name  # Имя текущего узла
        self.level = level  # Уровень узла в дереве
        self.children = []  # Список для хранения детей

def create_tree(data, parent=None, level=0):
    """
    Рекурсивно создает структуру дерева из вложенного словаря.

    Аргументы:
        data (dict): Словарь, содержащий информацию о текущем узле и его детях.
        parent (Person): Родительский узел текущего узла.
        level (int): Уровень текущего узла в дереве.

    Возвращает:
        Person: Созданный объект Person с его детьми.
    """
    if data:
        # Создаем новый объект Person для текущего узла
        member = Person(data['name'], parent, level)
        # Увеличиваем уровень для детей
        level += 1
        # Рекурсивно создаем детей
        member.children = [create_tree(child, member, level) for child in data.get('children', [])]
        return member

