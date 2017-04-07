__author__ = 'Balint'
"""nPuzzle Game Logic."""
from random import randint


class GameLogic(object):
    """Class for Game Logic."""

    def __init__(self, size):
        """Initialize."""
        super(GameLogic, self).__init__()
        self.size = size
        self.grid = []
        self.initialize_grid()
        # self.grid = [[13, 3, 5, 1], [2, 8, 0, 9], [4, 14, 12, 6], [7, 11, 15, 10]]


        # self.grid = [[15,0,7,5],[8,13,12,2],[3,1,4,9],[14,10,6,11]]
        # self.grid = [[11,12,5,6],[4,3,0,9],[2,8,1,7],[10,13,14,15]]

        # self.grid = [[1, 2, 3, 4],[5, 6, 7, 8], [9, 10, 0, 12],[13, 14, 11, 15]]


        self.grid = [[14,5,13,0],[4,7,8,9],[3,15,10,1],[11,2,12,6]]

        # self.grid = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 14], [13, 0, 15, 12]]

    def initialize_grid(self):
        """Initializing the underlying grid."""
        # All possible cell value.
        # 0 means, there is no tile at the cell.
        elements = []
        for i in range(self.size**2):
            elements.append(i)

        # Initialize all cell with value between 0 and 15.
        for i in range(self.size):
            self.grid.append([])
            for j in range(self.size):
                chosen_index = randint(0, len(elements) - 1)
                self.grid[i].append(elements[chosen_index])
                elements.pop(chosen_index)

    def step(self, x, y):
        """Take a step at given position."""
        if x > 0 and self.grid[x - 1][y] == 0:
            self.swap(x - 1, y, x, y)
        elif y < 3 and self.grid[x][y + 1] == 0:
            self.swap(x, y + 1, x, y)
        elif x < 3 and self.grid[x + 1][y] == 0:
            self.swap(x + 1, y, x, y)
        elif y > 0 and self.grid[x][y - 1] == 0:
            self.swap(x, y - 1, x, y)

    def swap(self, x1, y1, x2, y2):
        """Swapping two elements in the grid at the given positions."""
        self.grid[x1][y1] = self.grid[x2][y2]
        self.grid[x2][y2] = 0

    def print_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.grid[i][j], end=" ")
            print(" ")