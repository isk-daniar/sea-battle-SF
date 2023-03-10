from game import Game

# настройки игры в задании


# размер игрового поля
BOARD_SIZE = 6

# набор кораблей (размер, количество)
SHIP_SET = [(3, 1), (2, 2), (1, 4)]


# настройки стандартной игры


# размер игрового поля
# BOARD_SIZE = 10

# набор кораблей (размер, количество)
# SHIP_SET = [(4, 1), (3, 2), (2, 3), (1, 4)]

# старт игры

game = Game(board_size=BOARD_SIZE,
            ship_set=SHIP_SET)
game.start()
