import curses
import numpy as np
from random import randint, choice


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
    SNAKE_DEAD_CHAR = 'X'
    SNAKE_CHARS = {LeftDirection: 'L', RightDirection: 'R', UpDirection: 'U', DownDirection: 'D'}
    FOOD_CHARS = (u"\U0001F36B", u"\U0001F35F", u"\U0001F37A", u"\U0001F368", u"\U0001F351",
                  u"\U0001F355", u"\U0001F951")

    def __init__(self, rows, columns):
        self._rows = rows
        self._columns = columns
        self._game_over = False
        self._chars_to_replace = list(self.SNAKE_CHARS.values())
        self._setup_board()

        self.CHAR_TO_MOVEMENT = {
            'L': self._do_left_tail,
            'R': self._do_right_tail,
            'U': self._do_up_tail,
            'D': self._do_down_tail,
        }

        self.MOVEMENTS = {
            LeftDirection.__name__: self._do_left_head,
            RightDirection.__name__: self._do_right_head,
            UpDirection.__name__: self._do_up_head,
            DownDirection.__name__: self._do_down_head,
        }

    def _setup_board(self):
        self._board = np.full((self._rows, self._columns), self.EMPTY_CHAR)
        self._direction = RightDirection
        start = randint(1, self._rows - 2)
        self._head_r = start
        self._head_c = 1
        self._tail_r = start
        self._tail_c = 1
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
        for c in self._chars_to_replace:
            board[board == c] = self.SNAKE_BODY_CHAR
        self._fill_borders(board)
        board[self._head_r][self._head_c] = self.SNAKE_HEAD_CHAR if not self._game_over else self.SNAKE_DEAD_CHAR
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

    def _do_left_tail(self):
        self._tail_c -= 1

    def _do_right_tail(self):
        self._tail_c += 1

    def _do_up_tail(self):
        self._tail_r -= 1

    def _do_down_tail(self):
        self._tail_r += 1

    def _do_movement_head(self):
        self.MOVEMENTS[self._direction.__name__]()

    def _found_food(self):
        return self._board[self._head_r][self._head_c] in self.FOOD_CHARS

    def _update_head(self):
        self._board[self._head_r][self._head_c] = self.SNAKE_CHARS[self._direction]

    def _update_tail(self):
        move_to = self._board[self._tail_r][self._tail_c]
        self._board[self._tail_r][self._tail_c] = self.EMPTY_CHAR
        self.CHAR_TO_MOVEMENT.get(move_to)()

    def _put_food(self):
        r, c = randint(1, self._rows-2), randint(1, self._columns-7)
        if self._board[r][c] not in self.SNAKE_CHARS.values():
            self._board[r][c] = choice(self.FOOD_CHARS)
        else:
            self._put_food()

    def _end_game(self):
        self._game_over = True
        self._update_tail()
        self._board[self._head_r][self._head_c] = 'X'

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


def run(stdscr):

    def paint(b):
        board = b.get_board()
        for i, r in enumerate(board.T):
            for j, c in enumerate(r):
                stdscr.addstr(j, i, c)

    k = 0
    b = Board(20, 40)

    curses.start_color()
    stdscr = curses.initscr()
    stdscr.clear()
    curses.halfdelay(2)
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
    curses.wrapper(run)


if __name__ == "__main__":
    main()
