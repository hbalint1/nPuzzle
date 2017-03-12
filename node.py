__author__ = 'Balint'


class Node():
    """Node"""

    def __init__(self, grid, parent):
        self.grid = grid
        self.parent = parent
        self.gScore = 999