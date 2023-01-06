from dot import Dot


# класс корабля

class Ship:

    # инициализация корабля
    # вход:
    #   size - (int) размер корабля в точках
    #   location - (Dot) - координата головы
    #   direction - (int) - направление:
    #                       0 - вертикально вниз
    #                       1 - горизонтально вправо

    
    def __init__(self, size, location, direction):
        
        # размер корабля
        self.size = size
        
        # координата головы
        self.location = location
        
        # приращение (0, 1) - вертикально; (1, 0) - горизонтально
        self.increment = Dot(direction, 1 - direction)
        
        # количество жизней - осталось неподбитых точек
        self.lives = self.size

    # возврат точек корабля
    
    def dots(self):
        
        dot_list = list()
        dot = self.location
        
        for _ in range(0, self.size):
            dot_list.append(dot)
            dot += self.increment
        
        return dot_list
