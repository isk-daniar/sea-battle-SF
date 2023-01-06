import random

import error
from ship import Ship
from dot import Dot



# класс игрового поля

class Board:

    # приватные константы

    
    # флаги состояний клеток поля
    _STATE_SHOT = 1  # флаг стрельбы: 1 - была стрельба
    _STATE_BORDER = 2  # флаг бордюра: 1 - бордюр корабля
    _STATE_SHIP = 4  # флаг корабля: 1 - корабль
    
    # символы состояний клеток поля
    # поле бота
    _SYMBOL = [['_', 'T',
                '_', 'T',
                '_', 'X'],
    # поле игрока
               ['_', 'T',
                '_', 'T',
                '■', 'X']]
    
    # лимит попыток установки корабля
    _TRY_LIMIT = 100
    

    # инициализация поля

    def __init__(self, size):
        
        # размер игрового поля
        self.size = size
        
        # массив точек поля
        self.field = [[0 for x in range(self.size)] for y in range(self.size)]
        
        # список кораблей
        self.ships = list()
        
        # количество живых кораблей
        self.lives = 0
        
        # признак поля
        self.__mode = 0

    # признак отображения целых кораблей поля
    @property
    def mode(self):
        return self.__mode
    
    @mode.setter
    def mode(self, value):
        if 0 <= value <= 1:
            self.__mode = value

    # верхняя легенда для печати
    
    def get_legend(self):
        
        s = '\n AI:' + '  ' * (self.size-1) + 'Player:\n' + '  '
        for x in range(self.size):
            s += chr(ord('0') + x) + ' '
        s += '       '
        for x in range(self.size):
            s += chr(ord('0') + x) + ' '
        return s



    # строка поля для печати

    def get_line(self, y):
        
        s = chr(ord('A') + y) + '|'
        for x in range(self.size):
            s += self._SYMBOL[self.mode][self.field[x][y]] + "|"
        s += '    '
        return s


    # создать игровое поле

    def create(self, ship_set):
        
        while True:
            
            try:
                
                # инициализация массива точек поля
                self.field = [[0 for x in range(self.size)] for y in range(self.size)]
                
                # инициализация списка кораблей
                self.ships = list()
                
                # установить корабли на поле в соответствии с набором
                for ship_size, ships_number in ship_set:
                    
                    # установить корабль
                    for _ in range(ships_number):
                        
                        # счетчик попыток
                        try_cnt = 0
                        
                        while True:
                            
                            try:
                                
                                # отсчет попыток
                                try_cnt += 1
                                if try_cnt > self._TRY_LIMIT:
                                    raise error.TryLimit
                                
                                # сгенерировать корабль
                                ship = Ship(size=ship_size,
                                            location=Dot(x=random.randint(0, self.size - 1),
                                                         y=random.randint(0, self.size - 1)),
                                            direction=random.randint(0, 1))
                                
                                # добавить корабль на игровое поле
                                # если добавить невозможно -
                                # исключение Placement, новая попытка
                                self.add_ship(ship=ship)
                               
                                # ok
                                break
                            
                            except error.Placement:
                                pass
                break
            
            # лимит попыток генерации корабля -> генерация нового поля
            except error.TryLimit:
                pass
        
        # количество живых кораблей на поле
        self.lives = len(self.ships)


    # добавить корабль на поле:
    # проверить точки поля
    # установить корабль
    # обвести корабль бордюром
    # добавить корабль в список кораблей поля
    
    def add_ship(self, ship):
        
        # получить точки корабля
        dots = ship.dots()
        
        # проверить точки  на поле
        for dot in dots:
            
            # точка вне поля
            if dot.x >= self.size or dot.y >= self.size:
                raise error.Placement
            
            # точка занята
            if self.field[dot.x][dot.y] != 0:
                raise error.Placement
        
        # установить корабль
        for dot in dots:
            
            # точка корабля
            self.field[dot.x][dot.y] = self._STATE_SHIP
            
            # бордюр точки
            for offset in [(-1, -1), (0, -1), (1, -1),
                           (-1,  0),          (1,  0),
                           (-1,  1), (0,  1), (1,  1)]:
                x, y = dot.x + offset[0], dot.y + offset[1]
                # если точка существует и свободна
                if 0 <= x < self.size and \
                   0 <= y < self.size and \
                   self.field[x][y] == 0:
                    # определить ее как бордюр корабля
                    self.field[x][y] = self._STATE_BORDER
        
        # добавить корабль в список
        self.ships.append(ship)
    

    # получить состояние точки поля
    # для определения стрелял / не стрелял по этой точке

    def is_was_shot(self, dot):
        
        return self.field[dot.x][dot.y] & self._STATE_SHOT


    # выполнить выстрел:
    # отметить точку на поле как выстрел
    # если попал - найти корабль и уменьшить жизнь
    # определить количество живых кораблей

    def shot(self, dot):
        
        # отметить выстрел
        self.field[dot.x][dot.y] |= self._STATE_SHOT
        
        # мимо
        if self.field[dot.x][dot.y] != self._STATE_SHIP | self._STATE_SHOT:
            raise error.ShotPast
        
        # попал
        # найти корабль и уменьшить жизнь корабля
        [ship for ship in self.ships if dot in ship.dots()][0].lives -= 1
        
        # подсчет живых кораблей
        self.lives = sum(ship.lives for ship in self.ships)
        
        # ok
        raise error.ShotOk
