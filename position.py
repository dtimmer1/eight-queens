import numpy as np
from random import randint

NUM_QUEENS = 8  # n number of queens on an n x n board, can be changed
FITNESS_TABLE = [0, 0, 2, 6, 12, 18, 26, 34, 44, 56, 66, 78, 92]  # determine fitness values for n <= 11


class Position:
    def __init__(self, fitness=0, queens=np.zeros((NUM_QUEENS, 2))):
        self.fitness = fitness
        self.queens = queens

    def place_queens(self):
        # Generates a new position of eight queens on the board, sorted by first coordinate
        repeat = True
        for x in range(NUM_QUEENS):
            self.queens[x] = np.array([randint(0, NUM_QUEENS - 1), randint(0, NUM_QUEENS - 1)])
        while repeat:
            # eliminates duplicate queens to ensure eight unique queens
            check = True
            for i in range(len(self.queens)):
                for j in range(i + 1, len(self.queens)):
                    if np.array_equal(self.queens[i], self.queens[j]):
                        self.queens[i] = np.array([randint(0, NUM_QUEENS - 1), randint(0, NUM_QUEENS - 1)])
                        check = False
            if check:
                repeat = False
        self.queens = self.queens[np.argsort(self.queens[:, 0])]
        self.set_fitness()

    def render_helper(self, a, b):
        # checks if a queen in queens is at the given coordinates
        ret = False
        for q in self.queens:
            if np.array_equal(q, [a, b]):
                ret = True
        return ret

    def set_fitness(self):
        # Sets the fitness of this position. Fitness is defined by (44-fit)**2
        # where fit = the total number of queens on the same row, column, or diagonal
        # as each queen all summed together
        fit = 0
        for q in self.queens:
            for r in self.queens:
                if np.array_equal(q, r):
                    continue
                if q[0] == r[0] or q[1] == r[1] or abs(q[0] - r[0]) == abs(q[1] - r[1]):
                    # first two parameters check whether a queen is on the same rank and file
                    # as this queen, last one checks the diagonal (whether the difference of
                    # the coordinate vectors is in the span of [1, 1] or [1, -1]
                    fit += 1
        fit = (FITNESS_TABLE[NUM_QUEENS] - fit) ** 2
        self.fitness = fit

    def render(self):
        # goes through each row and column, if a queen has those coordinates print it
        alphabet = "abcdefghijklmnopqrstuvwxyz"  # this will serve for up to n = 26
        top_bar = "  "
        for i in range(NUM_QUEENS):
            top_bar = top_bar + " " + alphabet[i]
        print(top_bar)
        for x in range(NUM_QUEENS):
            board = str(NUM_QUEENS - x) + "  " if NUM_QUEENS - x < 10 else str(NUM_QUEENS - x) + " "
            for y in range(NUM_QUEENS):
                if self.render_helper(NUM_QUEENS - 1 - x, y):
                    board = board + "Q "
                else:
                    board = board + "  "
            print(board)
        self.set_fitness()
        print("fitness = " + str(self.fitness))
