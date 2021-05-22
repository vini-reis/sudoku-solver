from sudoku import *

def revise(csp : CSP, i : int, j : int):
    violate = [vi for vi in csp.D[i] if True not in {csp.test(i, vi, vj) for vj in csp.D[j]}]
    if len(violate) > 0:
        csp.D[i] = [v for v in csp.D[i] if v not in violate]
        csp.update(i)
        return True
    return False

def AC3(csp : CSP, queue : list):
    if len(queue) == 0: return csp

    i,j = queue.pop()
    if revise(csp, i, j):
        if not csp.valid(): return False
        [queue.append((k,i)) for k in csp.neighboors[i] if k != i and (k,i) not in queue]
        csp.update(i)
    return AC3(csp, queue)
