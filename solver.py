from node import Node
from enum import Enum
__author__ = 'Balint'
"""Automatic solving solutions."""


class AlgorithmTye(Enum):
    ASTAR = 1
    BREADTHFIRST = 2


class HeuristicType(Enum):
    MISPLACE = 1
    MANHATTAN = 2


class Solver(object):
    """Class for solving the nPuzzle game automatically."""
    def __init__(self, startstate, size):
        self.start_state = startstate
        self.size = size
        self.end_state = self.init_end()

    def init_end(self):
        end = []
        for i in range(self.size):
            end.append([])
            for j in range(self.size):
                end[i].append(i * self.size + j + 1)
        end[self.size - 1][self.size - 1] = 0
        # print(self.end_state)
        return end

    def run(self, algorithm, heuristic):
        if algorithm == AlgorithmTye.ASTAR:
            self.astar()
        elif algorithm == AlgorithmTye.BREADTHFIRST:
            self.breadth_first()

    def breadth_first(self):
        """Breadth First algorithm."""
        front = [[self.start_state]]
        expanded = []
        expanded_nodes = 0
        while front:
            i = 0
            for j in range(1, len(front)):    # minimum
                if len(front[i]) > len(front[j]):
                    i = j
            path = front[i]
            front = front[:i] + front[i+1:]
            endnode = path[-1]
            if endnode in expanded: continue
            for k in self.moves(endnode):
                if k in expanded: continue
                front.append(path + [k])
            expanded.append(endnode)
            expanded_nodes += 1
            if endnode == self.end_state:
                break
        print("Expanded nodes:", expanded_nodes)
        print("Solution:")
        # pp.pprint(path)

    def astar(self):
        """A* algorithm."""
        front = [[self.heuristic_2(self.start_state), self.start_state]]    # optional: heuristic_1
        expanded = []
        expanded_nodes = 0
        while front:
            i = 0
            for j in range(1, len(front)):
                if front[i][0] > front[j][0]:
                    i = j
            path = front[i]
            front = front[:i] + front[i+1:]
            endnode = path[-1]
            if endnode == self.end_state:
                break
            if endnode in expanded:
                continue
            for k in self.moves(endnode):
                if k in expanded:
                    continue
                newpath = [path[0] + self.heuristic_2(k) - self.heuristic_2(endnode)] + path[1:] + [k]
                front.append(newpath)
                if endnode not in expanded:
                    expanded.append(endnode)
            expanded_nodes += 1
            # if expanded_nodes % 1000 == 0:
            #     print(expanded_nodes)
        print("Expanded nodes:", expanded_nodes)
        print("Solution:")
        for i in path:
            print(i)
        # pp.pprint(path)

    def moves(self, mat):
        """Returns a list of all possible moves."""
        output = []

        # m = eval(mat)
        i = 0
        while 0 not in mat[i]:
            i += 1
        j = mat[i].index(0)   # blank space (zero)

        if i > 0:
            mat[i][j], mat[i-1][j] = mat[i-1][j], mat[i][j]  # move up
            output.append([x[:] for x in mat])
            mat[i][j], mat[i-1][j] = mat[i-1][j], mat[i][j]

        if i < self.size - 1:
            mat[i][j], mat[i+1][j] = mat[i+1][j], mat[i][j]   # move down
            output.append([x[:] for x in mat])
            mat[i][j], mat[i+1][j] = mat[i+1][j], mat[i][j]

        if j > 0:
            mat[i][j], mat[i][j-1] = mat[i][j-1], mat[i][j]   # move left
            output.append([x[:] for x in mat])
            mat[i][j], mat[i][j-1] = mat[i][j-1], mat[i][j]

        if j < self.size - 1:
            mat[i][j], mat[i][j+1] = mat[i][j+1], mat[i][j]   # move right
            output.append([x[:] for x in mat])
            mat[i][j], mat[i][j+1] = mat[i][j+1], mat[i][j]

        return output

    def heuristic_1(self, puzz):
        """Counts the number of misplaced tiles./Hamming distance"""
        misplaced = 0
        compare = 0
        # m = eval(puzz)
        for i in range(self.size):
            for j in range(self.size):
                if puzz[i][j] != compare:
                    misplaced += 1
                compare += 1
        return misplaced

    def heuristic_2(self, puzz):
        """Manhattan distance."""
        distance = 0
        # m = eval(puzz)
        for i in range(self.size):
            for j in range(self.size):
                value = puzz[i][j]
                if value == 0:
                    continue
                targetX = int((value - 1) / self.size)  # expected x-coordinate (row)
                targetY = int((value - 1) % self.size)  # expected y-coordinate (col)
                dx = i - targetX   # x-distance to expected coordinate
                dy = j - targetY   # y-distance to expected coordinate
                # print(value, abs(dx) + abs(dy))
                distance += abs(dx) + abs(dy)
                # distance += abs(i - (puzz[i][j] / self.size)) + abs(j - (puzz[i][j] % self.size))
                # print(distance)
        return distance


    def astar2(self, start, goal):
        """A* algorithm."""

        closed_set = []

        open_set = [start]

        start.gScore = 0
        start.fScore = self.heuristic_2(start.grid)
        expanded_nodes = 0
        while open_set:
            current = self.select_lowest_fScore(open_set)

            if current == goal:
                print(expanded_nodes)
                return self.reconstruct_path(current)

            open_set.remove(current)
            closed_set.append(current)

            for neighbor in self.moves2(current):
                if neighbor in closed_set:
                    continue

                tentative_gScore = current.gScore + 1

                # neighbor.gScore = self.heuristic_2(neighbor.grid)

                if neighbor not in open_set:
                    open_set.append(neighbor)
                elif tentative_gScore >= neighbor.gScore:
                    continue

                neighbor.gScore = tentative_gScore
                # f(n) = g(n) + h(n)
                neighbor.fScore = neighbor.gScore + self.heuristic_2(neighbor.grid)
            expanded_nodes += 1
            # if expanded_nodes % 1000 == 0:
            #     print(expanded_nodes)
            # print(len(open_set), len(closed_set))
        return None


    def moves2(self, node):
        """Returns a list of all possible moves."""
        output = []

        # m = eval(node)
        i = 0
        while 0 not in node.grid[i]:
            i += 1
        j = node.grid[i].index(0)   # blank space (zero)

        if i > 0:
            node.grid[i][j], node.grid[i-1][j] = node.grid[i-1][j], node.grid[i][j]  # move up
            output.append(Node([x[:] for x in node.grid], node))
            node.grid[i][j], node.grid[i-1][j] = node.grid[i-1][j], node.grid[i][j]

        if i < self.size - 1:
            node.grid[i][j], node.grid[i+1][j] = node.grid[i+1][j], node.grid[i][j]   # move down
            output.append(Node([x[:] for x in node.grid], node))
            node.grid[i][j], node.grid[i+1][j] = node.grid[i+1][j], node.grid[i][j]

        if j > 0:
            node.grid[i][j], node.grid[i][j-1] = node.grid[i][j-1], node.grid[i][j]   # move left
            output.append(Node([x[:] for x in node.grid], node))
            node.grid[i][j], node.grid[i][j-1] = node.grid[i][j-1], node.grid[i][j]

        if j < self.size - 1:
            node.grid[i][j], node.grid[i][j+1] = node.grid[i][j+1], node.grid[i][j]   # move right
            output.append(Node([x[:] for x in node.grid], node))
            node.grid[i][j], node.grid[i][j+1] = node.grid[i][j+1], node.grid[i][j]

        return output

    def reconstruct_path(self, node):
        nodes = [node]
        while node.parent is not None:
            nodes.append(node.parent)
            node = node.parent
        return nodes[::-1]

    def select_lowest_fScore(self, array):
        if len(array) == 0:
            return

        lowest = array[0]
        for i in array:
            if i.fScore < lowest.fScore:
                lowest = i

        return lowest





