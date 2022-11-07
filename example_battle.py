from random import randint


class Dot:
    def __init__(self, x, y):  # Класс точек на поле
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class BoardWrongShipException(BoardException):
    pass


class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow  # Длина корабля
        self.l = l  # Точка носа корабля
        self.o = o  # Направление корабля
        self.lives = l  # Сколько точек ещё не подбито

    @property
    def dots(self):
        ship_dots = []  # Список координат корабля
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))  # Добавление координат корабля в список координат корабля

        return ship_dots

    def shooten(self, shot):  # Функция определения попал ли выстрел в корабль
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size  # Размер доски
        self.hid = hid  # Параметр приятать доску или нет
        self.count = 0
        self.field = [["O"] * size for _ in range(size)]  # Переменная с генератором печатает 0
        self.busy = []
        self.ships = []

    def add_ship(self, ship):  # Метод ставит корабль на стол
        for d in ship.dots:  # Не понятно, почему ship.dots
            if self.out(d) or d in self.busy:  # Проверка исключения
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"  # Добавление обозначения корабля на стол
            self.busy.append(d)  # Добавление в список занятых клеток координаты точки с квадратом
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):  # Рисут точки вокруг корабля, чтобы проще было попадать дальше
        near = [
            (-1, -1), (-1, 0), (-1, 1),  # Список точек вокруг корабля
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):  # Выводит столбцы
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 "
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:  # Заменяет квадрат на ноль при вывод доски вашей
            res = res.replace("■", "O")
        return res

    def out(self, d):  # Определяет правильность координаты ввода
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):  # В случае выстрела за доску
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()  # Если клетка занята

        self.busy.append(d)  # Добавляет точку выстрела в список занятых клеток
        ships = 6

        for ship in self.ships:
            if d in ship.dots:  # Проверка если координаты выстрела совпадают с координатами корабля
                ship.lives -= 1  # Уменьшает счётчи жизней корабля
                self.field[d.x][d.y] = "X"  # ЗАменяет символ на доске
                if ship.lives == 0:  # Если корабль уничтожен
                    self.count += 1
                    self.contour(ship, verb=True)
                    ships -= 1
                    print("Корабль уничтожен!")
                    print(f"Осталось кораблей", ships)
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.x][d.y] = "T"  # В случае не совпадения
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()  # Исключение, возникающее в случаях, когда наследник класса не переопределил метод, который должен был

    def move(self):
        while True:
            try:  # Исключение
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):  # Ход противника случайными координатами
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()  # Зачем здесь split

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):  # Отлов ошибок в виде неправильного ввода данных
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()  # Определение доски игрокам
        co = self.random_board()
        co.hid = True  # Метод hid открывает вид вашей доски

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):  # Метод случайным образом расставляющий корабли
        lens = [3, 2, 2, 1, 1, 1, 1]  # Виды кораблей по длине
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):

        print("      Игра Морской бой  ")
        print(" первая цифра - номер строки  ")
        print(" вторая цифра - номер столбца ")

    def loop(self):
        num = 0  # Счётчик ходов
        while True:  # Цикл ходов
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1
    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()