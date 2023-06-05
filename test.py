import sys
import random
import argparse
from puzzle_BFS import PuzzleNode
import numpy as np
import os


def main():
    count_unsolvable=0
    count_case = 0
    all_steps = 0
    for i in range(20):
        for j in range(100):
            board = np.load(f'boards/{i}_{j}.npy')
            # print(board)
            status = list(board.flatten())
            # print(state)
            if os.path.exists(f'test/puzzle_{i}_{j}.txt'):
                with open(f'test/puzzle_{i}_{j}.txt', 'r') as fread:
                    lines = fread.readlines()
                num_nodes_check,num_nodes_expand,solution_step=0,0,0
                for line in lines:
                    if line[0:5]!='Total':
                        continue
                    if line.split(':')[0]=='Total nodes checked':
                        num_nodes_check = int(line.split(':')[1].split('\n')[0])
                    elif line.split(':')[0]=='Total nodes expanded':
                        num_nodes_expand = int(line.split(':')[1].split('\n')[0])
                    elif line.split(':')[0]=='Total solution steps':
                        solution_step = int(line.split(':')[1].split('\n')[0])
                all_steps += num_nodes_check
            else: 
                fout = open(f'test/puzzle_{i}_{j}.txt', 'w')
                temp = sys.stdout
                sys.stdout = fout
                puz = PuzzleNode(board.shape[0], status=status, log=False)
                solvable, num_inversions = puz.check_solvable()
                if solvable:
                    count_case +=1
                    num_nodes_check, num_nodes_expand, solution_path = puz.solve()
                    all_steps += num_nodes_check
                else:
                    count_unsolvable+=1
                    print('No Solution!')
                sys.stdout = temp
                fout.close()
    print(count_unsolvable,count_case, all_steps)
    print('average steps', float(all_steps/count_case))


if __name__ == '__main__':
    main()