from View.View import NPuzzle

__author__ = 'Balint'
"""nPuzzle game with Python."""

if __name__ == '__main__':
    # gameModel = GameLogic(4)
    # game = NPuzzle(gameModel)
    game = NPuzzle()
    # solver = Solver(game.model.grid, game.model.size)

    # print(solver.heuristic_2([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]))
    # print(solver.heuristic_2([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 0], [13, 14, 15, 12]]))
    # print(solver.heuristic_2([[14,5,13,0],[4,7,8,9],[3,15,10,1],[11,2,12,6]]))
    # print(solver.heuristic_2([[14,5,13,9],[4,7,8,0],[3,15,10,1],[11,2,12,6]]))
    # print(solver.heuristic_2([[14,5,13,9],[4,7,8,1],[3,15,10,0],[11,2,12,6]]))
    # print(solver.heuristic_2([[14,5,13,9],[4,7,8,1],[3,15,10,6],[11,2,12,0]]))

    # steps = solver.run(AlgorithmTye.ASTAR, 0)
    # asd = steps[1:]
    # for i in asd:
    #     print(i)
    # steps = solver.astar2(Node(game.model.grid, None),
    #                       Node([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]], None))
    # for n in steps:
    #     print(n.grid)
    game.run()