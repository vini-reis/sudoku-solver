import sys

from bfs import *
from dfs import *
from greedy import *
from astar import *
from ac3 import *
from backtracking import *

if __name__ == '__main__':
    # Lendo argumentos:
    filename = sys.argv[1]
    algorithm = sys.argv[2]

    if algorithm == "bfs":
        for board in read_board(filename):
            print(bfs(board))
    elif algorithm == "dfs":
        for board in read_board(filename):
            print(dfs(board))
    elif algorithm == "greedy":
        for board in read_board(filename):
            print(greedy(board,h1))
    elif algorithm == "astar":
        for board in read_board(filename):
            print(astar(board,g,h1))
    elif algorithm == "ac3":
        for board in read_board(filename):
            print(ac3(csp(board),worklist(board)))
    elif algorithm == "backtracking":
        for board in read_board(filename):
            print(backtracking(csp(board)))
