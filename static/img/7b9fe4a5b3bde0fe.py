WHITE = 1
BLACK = 2

def print_board(board):  # Распечатать доску в текстовом виде
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row + 1, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(chr(col + 65), end='    ')
    print()

def correct_coords(row, col):
    '''Функция проверяет, что координаты (row, col) лежат
    внутри доски'''
    return 0 <= row < 8 and 0 <= col < 8

def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE

def parse_coords(coords):
    # TODO функция должна принимать список координат в шахматном виде и возвращает row, col, row1, col1
    coords = coords.replace(" ","")
    coords = coords.upper()
    return int(coords[1])-1,ord(coords[0])-65,int(coords[3])-1, ord(coords[2])-65

class Board:
    def __init__(self):
        self.color = WHITE
        self.field = [[None] * 8 for row in range(8)]
#         заполнение доски фигурами
        for i in range(8):
            self.field[5][0] = Knight(WHITE)
            self.field[1][i] = Knight(WHITE)
            self.field[6][i] = Pawn(BLACK) 
        # TODO заполнить доску фигурами

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        '''Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела.'''
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]

    def move_piece(self, row, col, row1, col1):
        ''' Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False '''

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False

        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        else:
            # TODO Если мы перемещаемся на фигуру
            pass

        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        self.color = opponent(self.color) # поменять цвет
        return True

class Piece:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.not_moved = True

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(row, c) is None):
                return False
        self.moved()
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)

    def moved(self):
        self.not_moved = False

class Pawn(Piece):
    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if col != col1:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1 and board.field[row1][col1] is None:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True

        return False


class Knight(Piece):
    def char(self):
        return "K"

    def can_move(self,board,row,col,row1,col1):

        if abs(row - row1) == 2 and abs(col - col1) == 1 or abs(row - row1) == 1 and abs(col - col1) == 2:
            return True
        else:
            return False
        
    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)



def main():
    # Создаём доску
    board = Board()
    # Цикл ввода команд игроков
    while True:
        # Выводим доску
        print_board(board)
        # Подсказка по командам
        print('Команды:')
        print('    exit                               -- выход')
        print('    <coord1> <coord2>     -- ход из клетки (coord1) в клетку (coord2)')

        # Выводим чей ход
        if board.current_player_color() == WHITE:
            print('Ход белых: ', end='')
        else:
            print('Ход чёрных: ', end='')

        command = input()
        if command == 'exit':
            break

        row, col, row1, col1 = parse_coords(command)

        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')
main()