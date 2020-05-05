from ozobotmapf.mapf_solvers.solver import Solver


class ManualSolver(Solver):
    def __init__(self):
        pass

    def plan(self):
        plan = {1: {'pos_list': [0, 1, 3, 2, 0, 1, 3, 2, 0, 1, 3, 2, 0, 1, 3, 2], 'steps': [(0, 1), (1, 3), (3, 2), (2, 0), (0, 1), (1, 3), (3, 2), (2, 0), (0, 1), (1, 3), (3, 2), (2, 0), (0, 1), (1, 3), (3, 2)]}}
        return plan
