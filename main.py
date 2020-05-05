import emoji
import numpy as np
from random import randint
import time


class Direction:
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


class Board:

    SNAKE_CHAR = '\u2588'
    #FOOD_CHARS = ['\u1F951', 'U+1F346']

    DIRECTION_ALLOWED_FROM_MOVEMENT = {
        Direction.UP: (Direction.LEFT, Direction.RIGHT),
        Direction.DOWN: (Direction.LEFT, Direction.RIGHT),
        Direction.RIGHT: (Direction.UP, Direction.DOWN),
        Direction.LEFT: (Direction.UP, Direction.DOWN),
    }

    def __init__(self, rows, columns):
        self._rows = rows
        self._columns = columns
        self._board = np.zeros((rows, columns), dtype=str)
        start = 4#randint(0, rows)
        self._direction = Direction.RIGHT
        self._length = 1
        self._head_r = start
        self._head_c = 0
        self._tail_r = start
        self._tail_c = 0
        self._board[self._head_r][self._head_c] = self.SNAKE_CHAR

    def move(self, direction):
        if self._direction in self.DIRECTION_ALLOWED_FROM_MOVEMENT[direction]:
            self._direction = direction

    def get_board(self):
        return self._board.copy()

    def _check_boundaries(self):
        if self._head_r < 0 or self._head_r >= self._rows or self._head_c < 0 or self._head_c >= self._columns:
            raise Exception('Out of boundaries')

    def do(self):
        if self._direction == Direction.LEFT:
            self._head_c -= 1
        if self._direction == Direction.RIGHT:
            self._head_c += 1
        if self._direction == Direction.UP:
            self._head_r -= 1
        if self._direction == Direction.DOWN:
            self._head_r += 1

        self._check_boundaries()
        self._board[self._head_r][self._head_c] = self.SNAKE_CHAR
        self._board[self._tail_r][self._tail_c] = ''

        if self._direction == Direction.LEFT:
            self._tail_c -= 1
        if self._direction == Direction.RIGHT:
            self._tail_c += 1
        if self._direction == Direction.UP:
            self._tail_r -= 1
        if self._direction == Direction.DOWN:
            self._tail_r += 1




def main():
    b = Board(10, 10)

    for i in range(4):
        time.sleep(0.25)
        print(b.get_board())
        print()
        b.move(Direction.RIGHT)
        b.do()

    for i in range(4):
        time.sleep(0.25)
        print(b.get_board())
        print()
        b.move(Direction.DOWN)
        b.do()

    for i in range(4):
        time.sleep(0.25)
        print(b.get_board())
        print()
        b.move(Direction.RIGHT)
        b.do()

    for i in range(4):
        time.sleep(0.25)
        print(b.get_board())
        print()
        b.move(Direction.UP)
        b.do()

main()