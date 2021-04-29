from utils import *

def greedy(board,h):
    visited = set()
    nodes = expand(board)

    while nodes:
        node = min(nodes,key=h)
        if node not in visited and is_valid(node):
            sl = expand(node)
            # print(node) #debug
            for a in sl:
                if goal_reached(a): return a
        visited.add(node)
        nodes.remove(node)
        nodes.extend(sl)