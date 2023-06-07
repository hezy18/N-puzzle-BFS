# import heapq
import random
# from enum import Enum
from typing import List, Optional, Set
import numpy as np


class PuzzleNode:
    def __init__(self, n, status: Optional[List[int]] = None, log: bool = False,
                 parent=None, zero_pos: int = -1):
        self.n = n
        self.total_n = n * n
        self.parent: Optional[PuzzleNode] = parent
        # 0 代表空位
        if status is None:
            # random initialization
            self.status = list(range(self.total_n))
            random.shuffle(self.status)
        else:
            assert len(status) == self.total_n
            self.status = status
        if log:
            self.print_status()
        self.zero_pos = self.status.index(0) if zero_pos == -1 else zero_pos
        self.end_status = list(range(1,n*n))
        self.end_status.append(0)

    def print_status(self):
        print('Current Status:')
        for i in range(self.n):
            for j in range(self.n):
                pos = self.n * i + j
                print(f'{self.status[pos]: 3d}', end=' ')
            print()

    @staticmethod
    def get_fingerprint(status: List[int]) -> str:
        return ",".join([str(x) for x in status])

    def check_solvable(self):
        num_inversions = 0
        for i in range(self.total_n):
            for j in range(i + 1, self.total_n):
                x, y = self.status[i], self.status[j]
                num_inversions += int(x > y > 0)
        if self.n % 2 == 0:
            return (self.zero_pos // self.n + num_inversions) % 2 == 1, num_inversions
        else:
            return num_inversions % 2 == 0, num_inversions

    def solve(self):
        visited_forward: Set[str] = set()
        visited_backward: Set[str] = set()
        queue_forward: List[PuzzleNode] = [self]
        n = self.n
        queue_backward: List[PuzzleNode] = [PuzzleNode(n, status=self.end_status)]
        num_nodes_check, num_nodes_expand = 0, 2

        def step(nx, ny, is_forward):
            nonlocal num_nodes_expand
            # if is_forward:
            #     queue = queue_forward
            #     visited = visited_forward
                # root = queue_forward[-1]
            # else:
            #     queue = queue_backward
            #     visited = visited_backward
                # root = queue_backward[-1]

            new_pos = nx * n + ny
            new_status = root.status.copy()
            tmp = new_status[root.zero_pos]
            new_status[root.zero_pos] = new_status[new_pos]
            new_status[new_pos] = tmp
            assert tmp == 0
            fingerprint = PuzzleNode.get_fingerprint(new_status)
            if fingerprint in visited_forward or fingerprint in visited_backward:
                return
            new_node = PuzzleNode(n, status=new_status, parent=root, zero_pos=new_pos)
            if is_forward:
                queue_forward.append(new_node)
            else:
                queue_backward.append(new_node)
            num_nodes_expand += 1

        answer = None

        while len(queue_forward) > 0 and len(queue_backward) > 0:
            if len(queue_forward) <= len(queue_backward):
                root = queue_forward.pop(0)
                visited_forward.add(PuzzleNode.get_fingerprint(root.status))
                is_forward = True
                if PuzzleNode.get_fingerprint(root.status) in visited_backward:
                    # find the answer
                    answer = root
                    break
            else:
                root = queue_backward.pop(0)
                visited_backward.add(PuzzleNode.get_fingerprint(root.status))
                is_forward = False
                if PuzzleNode.get_fingerprint(root.status) in visited_forward:
                    # find the answer
                    answer = root
                    break         

            # check for possible nodes
            zero_pos = root.zero_pos
            zx, zy = zero_pos // n, zero_pos % n
            if zx > 0:
                step(zx - 1, zy, is_forward)
            if zx < n - 1:
                step(zx + 1, zy, is_forward)
            if zy > 0:
                step(zx, zy - 1, is_forward)
            if zy < n - 1:
                step(zx, zy + 1, is_forward)

            num_nodes_check += 1

        print("Total nodes checked:", num_nodes_check)
        print("Total nodes expanded:", num_nodes_expand)
        if answer is None:
            print('No Solution!')
            return None
        else:
            solution_path_forward = []
            solution_path_backward = []
            cur_node = answer
            while cur_node is not None:
                if PuzzleNode.get_fingerprint(cur_node.status) in visited_forward:
                    solution_path_forward.append(cur_node)
                else:
                    solution_path_backward.append(cur_node)
                cur_node = cur_node.parent

            solution_path_forward.reverse()
            # solution_path_backward.pop(0)
            solution_path_backward.reverse()
            solution_path = solution_path_forward + solution_path_backward

            print("Total solution steps:", len(solution_path) - 1)
            print('The solution path is:')
            res_path = []
            for node in solution_path:
                node.print_status()
                res_path.append(np.array(node.status).reshape((self.n, self.n)))
                print('\n' + '=' * 30 + '\n')
        return num_nodes_check, num_nodes_expand, res_path
