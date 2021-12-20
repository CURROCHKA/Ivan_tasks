from random import shuffle


def statistic(status):

    with open('statistic.txt', 'r') as s:
        old_data = s.read()
    old_data = old_data.split()
    if status:
        vic = int(old_data[1]) + 1
        los = int(old_data[3])
    else:
        vic = int(old_data[1])
        los = int(old_data[3]) + 1

    new_data = old_data
    new_data[1] = str(vic)
    new_data[3] = str(los)

    with open('statistic.txt', 'w') as s:
        for i in new_data:
            s.write(str(i))
            s.write('\n')


def correct_field(num_of_rows, num_of_columns, mines_number) -> bool:
    if all(i.isdigit() for i in [num_of_rows, num_of_columns, mines_number]) \
            and int(num_of_rows) > 0 and int(num_of_columns) > 0 and int(mines_number) > 0:
        return True
    print('Введите верные данные')
    return False


def correct_input(x: str, y: str, field: list) -> bool:
    if all(i.isdigit() for i in [x, y]) \
            and all(int(i) >= 0 for i in [x, y]) \
            and int(x) <= len(field) - 1 and int(y) <= len(field[0]) - 1:
        return True
    print('Введите верные координаты')
    return False


def is_mine(field: list, x: int, y: int) -> bool:
    if field[x][y] == 1:
        return True
    return False


def open_values(image: list) -> int:
    count_cell = 0

    for i in image:
        for j in i:
            if j != '#':
                count_cell += 1
    return count_cell


def calculate_value(field: list, x: int, y: int) -> int:
    mines = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= x + i < len(field) and 0 <= y + j < len(field[0]) and not (i == 0 and j == 0):
                if field[x + i][y + j] == 1:
                    mines += 1
    return mines


def new_image(field: list, image: list, x: int, y: int) -> list:
    new_value = calculate_value(field, x, y)
    image[x][y] = str(new_value)
    return image


def failed_image(field: list, image: list) -> list:
    for i, sublist in enumerate(field):
        for j, cell in enumerate(sublist):
            if cell == 1:
                image[i][j] = '*'
    return image


def show_image(image):
    for i in image:
        print(' '.join(i))


def make_move(field: list, image: list):
    x, y = input('Введите номер строки: '), input('Введите номер столбца: ')
    if not correct_input(x, y, field):
        return image, True

    # is clicked ???
    # if yes
    # return image, True
    x = int(x)
    y = int(y)
    if is_mine(field, x, y):
        print('Game over!')
        statistic(False)
        image = failed_image(field, image)
        show_image(image)
        return image, False
    else:
        image = new_image(field, image, x, y)
        return image, True


def generate_field(num_of_rows: str, num_of_columns: str, mines_number: str) -> tuple:
    present_field = []
    temp_list = []
    image = [['#' for _ in range(int(num_of_columns))] for _ in range(int(num_of_rows))]
    field = [0] * (int(num_of_rows) * int(num_of_columns) - int(mines_number)) + [1] * int(mines_number)
    shuffle(field)
    for i, j in enumerate(field):
        if not (i + 1) % int(num_of_columns):
            temp_list.append(j)
            present_field.append(temp_list)
            temp_list = []  # метод clear() здесь не работает
        else:
            temp_list.append(j)
    return present_field, image


def is_finish():
    pass


def start_game():
    num_of_rows, num_of_columns, mines_number = difficult_lvl()
    field, image = generate_field(num_of_rows, num_of_columns, mines_number)
    game_status = True

    while game_status:
        if open_values(image) == int(num_of_rows) * int(num_of_columns) - int(mines_number):
            print('Победа!')
            statistic(True)
            failed_image(field, image)
            show_image(image)
            game_status = False
        else:
            show_image(image)
            image, game_status = make_move(field, image)


def diff_custom() -> tuple:
    diff_status = True
    while diff_status:
        num_of_rows, num_of_columns = input('Введите кол-во строк: '), input('Введите кол-во столбцов: ')
        mines_number = input('Введите кол-во мин: ')
        if correct_field(num_of_rows, num_of_columns, mines_number):
            diff_status = False
    return num_of_rows, num_of_columns, mines_number


def difficult_lvl() -> tuple:
    easy = (3, 3, 3)
    medium = (5, 5, 7)
    hard = (7, 7, 18)
    difficult_input = ''
    difficult = ''
    while difficult_input not in ['1', '2', '3', '4']:
        difficult_input = input('Выберите уровень сложонсти:\neasy - 1;\nmedium - 2;\nhard - 3;\ncustom - 4\n')
        if difficult_input == '1':
            difficult = easy
        elif difficult_input == '2':
            difficult = medium
        elif difficult_input == '3':
            difficult = hard
        elif difficult_input == '4':
            difficult = diff_custom()
    return difficult


def is_new_game() -> bool:
    new_game_status = True
    while new_game_status:
        print('Новая игра: Y', 'Завершить игру: N', 'Посмотреть статистику: S', sep='\n')
        string = input()
        if string.lower() == 'y':
            return True
        elif string.lower() == 'n':
            return False
        elif string.lower() == 's':
            with open('statistic.txt', 'r') as s:
                print(s.read())


def main():
    while is_new_game():
        start_game()


main()
