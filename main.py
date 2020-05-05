import curses
import numpy as np
from random import randint, choice
import time


class LeftDirection:

    @staticmethod
    def move_left():
        return LeftDirection

    @staticmethod
    def move_right():
        return LeftDirection

    @staticmethod
    def move_up():
        return UpDirection

    @staticmethod
    def move_down():
        return DownDirection


class RightDirection:

    @staticmethod
    def move_left():
        return RightDirection

    @staticmethod
    def move_right():
        return RightDirection

    @staticmethod
    def move_up():
        return UpDirection

    @staticmethod
    def move_down():
        return DownDirection


class UpDirection:

    @staticmethod
    def move_left():
        return LeftDirection

    @staticmethod
    def move_right():
        return RightDirection

    @staticmethod
    def move_up():
        return UpDirection

    @staticmethod
    def move_down():
        return UpDirection


class DownDirection:

    @staticmethod
    def move_left():
        return LeftDirection

    @staticmethod
    def move_right():
        return RightDirection

    @staticmethod
    def move_up():
        return DownDirection

    @staticmethod
    def move_down():
        return DownDirection


class Board:

    SNAKE_HEAD_CHAR = u"\u0040"
    SNAKE_BODY_CHAR = u"\u006F"
    EMPTY_CHAR = u"\u0020"
    SNAKE_CHARS = {LeftDirection: 'L', RightDirection: 'R', UpDirection: 'U', DownDirection: 'D'}
    FOOD_CHARS = (u"\U0001F36B", u"\U0001F35F", u"\U0001F373", u"\U0001F37A", u"\U0001F368", u"\U0001F351",
                  u"\U0001F355", u"\U0001F951")

    def __init__(self, rows, columns):
        self._rows = rows
        self._columns = columns
        self._board = np.full((rows, columns), self.EMPTY_CHAR)
        self._direction = RightDirection
        start = randint(1, rows - 2)
        self._head_r = start
        self._head_c = 1
        self._tail_r = start
        self._tail_c = 1
        self._game_over = False

        self.MOVEMENTS = {
            LeftDirection.__name__: self._do_left_head,
            RightDirection.__name__: self._do_right_head,
            UpDirection.__name__: self._do_up_head,
            DownDirection.__name__: self._do_down_head,
        }
        self._put_food()

    def _fill_borders(self, board):
        board[0] = '━'
        board[-1] = '━'
        board.T[0] = '┃'
        board.T[-1] = '┃'
        board[0][0] = '┏'
        board[self._rows-1][0] = '┗'
        board[0][self._columns-1] = '┓'
        board[-1][-1] = '┛'

    def move_left(self):
        self._direction = self._direction.move_left()

    def move_right(self):
        self._direction = self._direction.move_right()

    def move_up(self):
        self._direction = self._direction.move_up()

    def move_down(self):
        self._direction = self._direction.move_down()

    def get_board(self):
        board = self._board.copy()
        chars_to_replace = list(self.SNAKE_CHARS.values())
        for c in chars_to_replace:
            board[board == c] = self.SNAKE_BODY_CHAR
        board[self._head_r][self._head_c] = self.SNAKE_HEAD_CHAR
        self._fill_borders(board)
        return board

    def _check_conflicts(self):
        if self._head_r <= 0 or self._head_r >= self._rows-1 or self._head_c <= 0 or self._head_c >= self._columns-1:
            raise RuntimeError('Out of boundaries')
        if self._board[self._head_r][self._head_c] in self.SNAKE_CHARS.values():
            raise RuntimeError('Ate your tail')

    def _do_left_head(self):
        self._head_c -= 1

    def _do_right_head(self):
        self._head_c += 1

    def _do_up_head(self):
        self._head_r -= 1

    def _do_down_head(self):
        self._head_r += 1

    def _do_movement_head(self):
        self.MOVEMENTS[self._direction.__name__]()

    def _found_food(self):
        return self._board[self._head_r][self._head_c] in self.FOOD_CHARS

    def _update_head(self):
        self._board[self._head_r][self._head_c] = self.SNAKE_CHARS[self._direction]

    def _update_tail(self):
        move_to = self._board[self._tail_r][self._tail_c]
        self._board[self._tail_r][self._tail_c] = self.EMPTY_CHAR
        if move_to == 'L':
            self._tail_c -= 1
        elif move_to == 'R':
            self._tail_c += 1
        elif move_to == 'U':
            self._tail_r -= 1
        elif move_to == 'D':
            self._tail_r += 1

    def _put_food(self):
        r, c = randint(1, self._rows-2), randint(1, self._columns-2)
        if self._board[r][c] not in self.SNAKE_CHARS.values():
            self._board[r][c] = choice(self.FOOD_CHARS)
        else:
            self._put_food()

    def _end_game(self):
        self._game_over = True

    def play(self):
        if self._game_over:
            return

        self._update_head()
        self._do_movement_head()

        try:
            self._check_conflicts()
        except RuntimeError as e:
            self._end_game()
            return

        found_food = self._found_food()
        self._update_head()

        if found_food:
            self._put_food()
        else:
            self._update_tail()


def start(stdscr):

    def paint(b):
        board = b.get_board()
        for i, r in enumerate(board.T):
            for j, c in enumerate(r):
                stdscr.addstr(j, i, c)

    k = 0
    b = Board(20, 40)

    stdscr = curses.initscr()
    stdscr.clear()
    stdscr.keypad(True)

    MOVE_KEYS = {curses.KEY_LEFT: b.move_left,
                 curses.KEY_RIGHT: b.move_right,
                 curses.KEY_UP: b.move_up,
                 curses.KEY_DOWN: b.move_down}

    while k != ord('q'):
        paint(b)
        k = stdscr.getch()
        if k in MOVE_KEYS:
            MOVE_KEYS.get(k)()
        b.play()


def main():
    curses.wrapper(start)


if __name__ == "__main__":
    main()