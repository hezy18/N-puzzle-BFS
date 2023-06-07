from puzzle_BFS import PuzzleNode
import numpy as np


def frontend_solve(inputs: np.ndarray):
    """
    :param inputs: the initial state, shape [n, n], numbered 0~(n^2-1)
    :return: if solvable, return (search step count, expanded node count, the solution path)
             The solution path includes the initial state and the target state
             if unsolvable, return None
    """
    status = list(inputs.flatten())
    n = inputs.shape[0]
    puz = PuzzleNode(n, status=status, log=False)
    solvable, num_inversions = puz.check_solvable()
    if solvable:
        return puz.solve()
    else:
        return None

# example
x = np.array([[1, 2, 3], [4, 5, 0], [7, 8, 6]])
num_nodes_check, num_nodes_expand, res_path = frontend_solve(x)
for res in res_path:
    print(res)
            

