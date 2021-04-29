from utils import *

def bfs(board):
    visitados = set()
    fila = [board,]

    while fila:
        s = fila.pop(0)
        if s not in visitados and is_valid(s):
            if goal_reached(s):
                return s
            visitados.add(s)
            # print(s) #debug
            fila.extend(expand(s))
            fila.sort(key=cost)
