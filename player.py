import random
import time

from dot import Dot
from board import Board
import error


# суперкласс игрока


class Player:

    # инициализация игрока

    def __init__(self, board_size, ship_set):
        
        self.board = list()
        self.board_size = board_size
        self.ship_set = ship_set

    # приватные атрибуты

    # координаты хода
    _shot = Dot(0, 0)

    # сформировать игровое поле
    # и выставить корабли согласно списка
    
    def make_board(self, mode):
        
        self.board = Board(size=self.board_size)
        self.board.create(ship_set=self.ship_set)
        self.board.mode = mode

    # сделать ход
    def move(self):
        
        # сделать выстрел
        try:
            self.board.shot(self._shot)
            
        except error.ShotPast:
            print('\nМимо')
            
        except error.ShotOk:
            print('\nП О П А Л !!!')
    
    # -------------------------------------------
    # контроль игровой ситуации
    # -------------------------------------------
    
    def check(self):
        
        # проверить количество осташихся кораблей
        if self.board.lives == 0:
            # игра окончена
            raise error.GameOver
    
    # -------------------------------------------
    # запросить ход
    # -------------------------------------------
    
    def ask(self):
        pass


# -------------------------------------------
# класс игрока
# -------------------------------------------

class User(Player):
    
    # -------------------------------------------
    # запросить ход у игрока
    # -------------------------------------------
    
    def ask(self):

        while True:
            
            try:
                # получить строку ответа y, x
                s = input('\nВаш ход (YX): ').lower()
                
                # сохранить координаты - x, y
                self._shot = Dot(ord(s[1])-ord('0'), ord(s[0])-ord('a'))
                
                # выстрел за пределами поля
                if not 0 <= self._shot.x < self.board_size or \
                   not 0 <= self._shot.y < self.board_size:
                    raise error.OutOfBoard
                
                # выстрел уже был
                if self.board.is_was_shot(self._shot):
                    raise error.AlreadyShot
                
                # ok
                break
                
            except error.OutOfBoard:
                print('За пределами поля')
                
            except error.AlreadyShot:
                print('Выстрел уже был')
                
            except:
                print('Повторите ввод')


# -------------------------------------------
# вспомогательная функция задержки вывода символа
# -------------------------------------------

def _delay():
    
    for i in '|/-\\|':
        print(i, end='')
        time.sleep(0.3)
        print(chr(8), end='')
    
    
# -------------------------------------------
# класс бота
# -------------------------------------------

class Bot(Player):
    
    # -------------------------------------------
    # запрос хода бота
    # -------------------------------------------
    
    def ask(self):
    
        # получить точку на поле
        while True:
            
            # сгенерировать новую точку
            dot = Dot(x=random.randint(0, self.board_size - 1),
                      y=random.randint(0, self.board_size - 1))
            
            # установить ее, если поле свободно
            if not self.board.is_was_shot(dot):
                break
        
        # запомнить точку
        self._shot = dot
        
        # сообщить ход бота
        print('\nМой ход: ', end='')
        _delay()
        print(chr(ord('A')+self._shot.y), end='')
        _delay()
        print(self._shot.x)
        time.sleep(0.5)
