import emoji
import numpy as np
from random import randint
import time


class LeftDirection:

    def move_left(self):
        return LeftDirection

    def move_right(self):
        return LeftDirection

    def move_up(self):
        return UpDirection

    def move_down(self):
        return DownDirection


class RightDirection:

    def move_left(self):
        return RightDirection

    def move_right(self):
        return RightDirection

    def move_up(self):
        return UpDirection

    def move_down(self):
        return DownDirection


class UpDirection:

    def move_left(self):
        return LeftDirection

    def move_right(self):
        return RightDirection

    def move_up(self):
        return UpDirection

    def move_down(self):
        return UpDirection


class DownDirection:

    def move_left(self):
        return LeftDirection

    def move_right(self):
        return RightDirection

    def move_up(self):
        return DownDirection

    def move_down(self):
        return DownDirection


class Board:

    SNAKE_CHAR = '\u2588'
    FOOD_CHAR = 'X'
    #FOOD_CHARS = ['\u1F951', 'U+1F346']

    def __init__(self, rows, columns):
        self._rows = rows
        self._columns = columns
        self._board = np.full((rows, columns), ' ')
        start = randint(0, rows)
        self._direction = RightDirection
        self._length = 1
        self._head_r = start
        self._head_c = 0
        self._tail_r = start
        self._tail_c = 0
        self._board[self._head_r][self._head_c] = self.SNAKE_CHAR
        self._put_food()
        self._time = 0

        self.MOVEMENTS = {
            LeftDirection.__name__: (self._do_left_head, self._do_left_tail),
            RightDirection.__name__: (self._do_right_head, self._do_right_tail),
            UpDirection.__name__: (self._do_up_head, self._do_up_tail),
            DownDirection.__name__: (self._do_down_head, self._do_down_tail),
        }

    def move_left(self):
        self._direction = self._direction().move_left()

    def move_right(self):
        self._direction = self._direction().move_right()

    def move_up(self):
        self._direction = self._direction().move_up()

    def move_down(self):
        self._direction = self._direction().move_down()

    def get_board(self):
        return self._board.copy()

    def _check_boundaries(self):
        if self._head_r < 0 or self._head_r >= self._rows or self._head_c < 0 or self._head_c >= self._columns:
            raise Exception('Out of boundaries')

    def _eat(self):
        self._length += 1

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
        self.MOVEMENTS[self._direction.__name__][0]()

    def _do_movement_tail(self):
        self.MOVEMENTS[self._direction.__name__][1]()

    def _found_food(self):
        return self._board[self._head_r][self._head_c] == self.FOOD_CHAR

    def _update_head(self):
        self._board[self._head_r][self._head_c] = self.SNAKE_CHAR

    def _update_tail(self):
        self._board[self._tail_r][self._tail_c] = ' '

    def _put_food(self):
        r, c = randint(0, self._rows-1), randint(0, self._columns-1)
        if self._board[r][c] != self.SNAKE_CHAR:
            self._board[r][c] = self.FOOD_CHAR
        else:
            self._put_food()

    def play(self):
        self._time += 1

        self._do_movement_head()
        self._check_boundaries()

        if self._found_food():
            self._length += 1
            self._update_head()
            self._put_food()
        else:
            self._update_tail()
            self._do_movement_tail()
            self._update_head()



def main():
    b = Board(10, 10)

    for i in range(10):
        time.sleep(0.25)
        print(b.get_board())
        print()
        b.move_up()
        b.play()


main()