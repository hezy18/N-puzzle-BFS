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
        close_list: Set[str] = set()
        open_list: List[PuzzleNode] = [self]
        n, num_nodes_check, num_nodes_expand = self.n, 0, 1

        def step(nx, ny):
            nonlocal num_nodes_expand
            new_pos = nx * n + ny
            # get the exchange status
            new_status = root.status.copy()
            tmp = new_status[zero_pos]
            new_status[zero_pos] = new_status[new_pos]
            new_status[new_pos] = tmp
            assert tmp == 0
            if PuzzleNode.get_fingerprint(new_status) in close_list:
                return
            new_node = PuzzleNode(n, status=new_status, parent=root, zero_pos=new_pos)
            open_list.append(new_node)
            num_nodes_expand += 1

        answer = None
        
        while len(open_list) > 0:
            root = open_list.pop(0)
            if root.status == self.end_status:
                # find the answer
                answer = root
                break
            # check for possible nodes
            zero_pos = root.zero_pos
            zx, zy = zero_pos // n, zero_pos % n
            if zx > 0:
                step(zx - 1, zy)
            if zx < n - 1:
                step(zx + 1, zy)
            if zy > 0:
                step(zx, zy - 1)
            if zy < n - 1:
                step(zx, zy + 1)
            close_list.add(PuzzleNode.get_fingerprint(root.status))
            num_nodes_check += 1

        print("Total nodes checked:", num_nodes_check)
        print("Total nodes expanded:", num_nodes_expand)
        if answer is None:
            print('No Solution!')
            return None
        else:
            solution_path = []
            cur_node = answer
            while cur_node is not None:
                solution_path.append(cur_node)
                cur_node = cur_node.parent
            solution_path.reverse()
            print("Total solution steps:", len(solution_path) - 1)
            print('The solution path is:')
            res_path = []
            for node in solution_path:
                node.print_status()
                res_path.append(np.array(node.status).reshape((self.n, self.n)))
                print('\n' + '=' * 30 + '\n')
        return num_nodes_check, num_nodes_expand, res_path