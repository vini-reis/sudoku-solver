from utils import *

def dfs(board):
    visited = set()
    visited.add(board)
    if goal_reached(board): return board
    queue = [board]
    while queue:
        state = queue.pop()
        for s in expand(state):
            if s not in visited and is_valid(s):
                # print(s) #debug
                if goal_reached(s): return s
                visited.add(s)
                queue.append(s)
    return None