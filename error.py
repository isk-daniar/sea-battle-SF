# классы исключений

# лимит попыток исчерпан
class TryLimit(Exception):
    pass


# ошибка размещения корабля
class Placement(Exception):
    pass


# выстрел уже был
class AlreadyShot(Exception):
    pass


# выстрел за пределами поля
class OutOfBoard(Exception):
    pass


# выстрел мимо
class ShotPast(Exception):
    pass


# удачный выстрел
class ShotOk(Exception):
    pass


# не цифровой символ
class NotDigit(Exception):
    pass


# игра окончена
class GameOver(Exception):
    pass
