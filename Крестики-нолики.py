
print('Правила: первой число для ввода - строка, второе- столбик')

def board():
    print(f'  0 1 2 ')
    print(f'0 {field[0][0]} {field[0][1]} {field[0][2]}')
    print(f'1 {field[1][0]} {field[1][1]} {field[1][2]}')
    print(f'2 {field[2][0]} {field[2][1]} {field[2][2]}')
def turn():
    while True:
        coordinati = input(" Куда воткнуть, формат x пробел y:").split()
        if len(coordinati) != 2:
            print('Введите две координаты')
            continue
        x,  y = coordinati
        if not(x.isdigit) or not(y.isdigit):
            print('Введите цифры')
            continue
        x, y = int(x), int(y)
        if 0 > x or x > 2 or 0 > y or y > 2:
            print(" Координаты вне диапазона! ")
            continue

        if field[x][y] != " ":
            print(" Клетка занята! ")
            continue
        return x, y

def win():
    win_res = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
    for res in win_res:
        symbols = []
        for c in res:
            symbols.append(field[c[0]][c[1]])
        if symbols == ["X", "X", "X"]:
            print("Выиграл X!!!")
            return True
        if symbols == ["0", "0", "0"]:
            print("Выиграл 0!!!")
            return True
    return False


field = [[" "] * 3 for i in range(3)]
count = 0
while True:
    count += 1
    board()
    if count % 2 == 1:
        print(" Ходит крестик!")
    else:
        print(" Ходит нолик!")
    x, y = turn()
    if count % 2 == 1:
        field[x][y] = "X"
    else:
        field[x][y] = "0"
    if win():
        break
    if count == 9:
        print(" Ничья!")
        break







