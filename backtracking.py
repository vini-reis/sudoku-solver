import numpy as np
from copy import copy

from sudoku import *

def selectVar(csp : CSP) -> int:
    count = [len(csp.C[c]) if c in csp.X else 0 for c in range(81)]
    return np.argmax(count)

def sortValues(i : int, csp : CSP):
    count = [(len([True for k in csp.neighboors[i] if v in csp.D[k] and k in csp.X]), v) for v in csp.D[i]]
    count = sorted(count, reverse=True)
    return [v[1] for v in count]

def assign(v, i, csp : CSP):
    csp_novo : CSP = copy(csp)
    csp_novo.D[i] = [v]
    csp_novo.update(i)
    if csp_novo.valid() and csp_novo.check():
        return True, csp_novo
    return False, csp

def backtracking(csp : CSP):
    if not csp.valid(): return False
    if len(csp.X) == 0 and csp.check(): return csp

    i = selectVar(csp)
    for v in sortValues(i, csp):
        consistent, sol = assign(v, i, csp)
        if consistent:
            sol = backtracking(sol)
            if sol: return sol
    return False