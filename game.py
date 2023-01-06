import random

import error
import player



# класс игры


class Game:
    

    # приватные константы

    _MODE_USER = 0
    _MODE_BOT = 1

    # инициализация игры
    
    def __init__(self, board_size, ship_set):
        
        self.board_size = board_size
        self.ship_set = ship_set

    # печать игровых полей

    def __print_board(self, right_board, left_board):
        
        print(right_board.get_legend())
        for y in range(self.board_size):
            print(right_board.get_line(y), left_board.get_line(y))

    # приветствие
    
    def greet(self):
        
        print()
        print("*********************************")
        print("*                               *")
        print("*       Приветствую Вас!        *")
        print("*    Вы в игре 'Морской бой'    *")
        print("*                               *")
        print("*********************************")

    # игра
    
    def loop(self):
        
        # определить игроков
        user = player.User(board_size=self.board_size,
                           ship_set=self.ship_set)
        bot = player.Bot(board_size=self.board_size,
                         ship_set=self.ship_set)
        
        # главный цикл
        while True:
            
            # запрос новой игры
            if input('\nНачать новую игру? (n - нет)').lower() == 'n':
                print("\nBye!")
                break
            
            # сформировать игровые поля
            user.make_board(mode=self._MODE_USER)
            bot.make_board(mode=self._MODE_BOT)
                
            # цикл игры
            while True:
                    
                # игра игрока
                try:
                    self.__print_board(right_board=user.board,
                                       left_board=bot.board)
                    user.ask()
                    user.move()
                    user.check()
                
                except error.GameOver:
                    print("\nПоздравляю. Вы выиграли.")
                    break
                    
                # игра бота
                try:
                    self.__print_board(right_board=user.board,
                                       left_board=bot.board)
                    bot.ask()
                    bot.move()
                    bot.check()
                
                except error.GameOver:
                    print("\nПоздравьте меня. Я выиграл.")
                    break

            print("\nИгра окончена.")
            self.__print_board(right_board=user.board,
                               left_board=bot.board)

    # старт игры
    
    def start(self):
        
        random.seed()
        self.greet()
        self.loop()
