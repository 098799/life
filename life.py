import collections
import os
import random
import sys
import time

import watchgod


size_x = 55
size_y = 110
offset_x = 30
offset_y = 30
refresh_rate = 0.1


def neighbours(position):
    x, y = position
    return {
        (pos[0] % size_x, pos[1] % size_y)
        for pos in {
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
            (x + 1, y + 1),
            (x - 1, y - 1),
            (x + 1, y - 1),
            (x - 1, y + 1),
        }
    }


def iterate(ones):
    all_neighbors = set(neighbour for cell in ones for neighbour in neighbours(cell)) - ones
    ones_copy = ones.copy()

    for cell in ones_copy:
        status = len(ones_copy & neighbours(cell))

        if status < 2 or status >= 4:
            ones.remove(cell)

    for neighbour in all_neighbors:
        status = len(neighbours(neighbour) & ones_copy)

        if status == 3:
            ones.add(neighbour)

    return ones


def draw_board(ones):
    board = []

    for i in range(size_x):
        board.append([" "] * size_y)

    for one in ones:
        x_coord = (one[0] + offset_x) % size_x
        y_coord = (one[1] + offset_y) % size_y
        board[x_coord][y_coord] = "\u2588"

    return "\n".join(["".join(row) for row in board])


def input_read(filename):
    with open(filename, "r") as input_file:
        contents = input_file.read()

    ones = set()

    for index, row in enumerate(contents.split("\n")):
        for row_index, character in enumerate(row):
            if character == "1":
                ones.add((index, row_index))

    return ones


def random_board():
    ones = set()

    for i in range(size_x):
        for j in range(size_y):
            if random.randint(0, 4) == 2:
                ones.add((i, j))

    return ones


def life():
    ones = input_read(filename)
    # ones = random_board()
    queue = collections.deque()

    while True:
        os.system("clear")
        board = draw_board(ones)
        print(board)

        if board in queue:
            return

        if len(queue) > 7:
            queue.popleft()

        queue.append(board)
        ones = iterate(ones)
        time.sleep(refresh_rate)


filename = sys.argv[1]


watchgod.run_process(filename, life)
