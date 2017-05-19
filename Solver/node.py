__author__ = 'Balint'


class Node():
    """Node"""

    def __init__(self, grid, parent):
        self.grid = grid
        self.parent = parent
        self.gScore = 999
        self.fScore = 999

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.grid == other.grid

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(tuple(sorted(self.__dict__.items())))