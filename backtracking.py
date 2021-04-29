import numpy as np

from utils import *
from ac3 import *

class Board():
    def __init__(self, state):
        self._rows = np.array([[int(state[i+j*9]) if state[i+j*9] != '.' else 0 for i in range(9)] for j in range(9)])
        self._cols = np.array([[self._rows[i][j] for i in range(9)] for j in range(9)])
        self._boxs = np.array([[self._rows[i+3*l][j+3*k] for i in range(3) for j in range(3)] for l in range(3) for k in range(3)])

    def __str__(self):
        return "".join(self._rows.flatten())

    def getRow(self, row) -> list or None:
        return self._rows[row] if row >= 0 & row < 9 else None

    def getColumn(self, col) -> list or None:
        return self._cols[col] if col >= 0 & col < 9 else None
    
    def getBox(self, box) -> list or None:
        return self._boxs[box] if box >= 0 & box < 9 else None

    def check(self) -> bool:
        for row in self._rows:
            v = set()
            for i in row:
                if i not in v: 
                    v.add(i)
                else: 
                    return False
        for col in self._cols:
            v = set()
            for i in col:
                if i not in v:
                    v.add(i)
                else:
                    return False
        for box in self._boxs:
            v = set()
            for i in box:
                if i not in v:
                    v.add(i)
                else:
                    return False
        return True

def selectVar(csp1):
    # sizes = [(len(csp1.D[x]),x) for x in range(len(csp1.D)) if (len(csp1.D[x])) > 1]
    # sizes = sorted(sizes)
    # return sizes[0][1]
    consts = worklist(csp1)
    c_count = [(len([(x,y) for x,y in consts if x == i]),i) if str(csp1)[i] == '.' else (0,i) for i in range(len(csp1.D))]
    c_count = sorted(c_count, reverse=True)
    return c_count[0][1]

def sortValues(i,csp1):
    violate_count = [(len([True for y in neighboors(i,csp1) if x in csp1.D[y]]),x) for x in csp1.D[i]]
    violate_count = sorted(violate_count)
    violations = [x[1] for x in violate_count]
    return violations

def allSingle(csp1):
    for d in csp1.D:
        if len(d) > 1: return False
    return True

def anyEmpty(csp1):
    for d in csp1.D:
        if len(d) < 1: return True
    return False

def assign(x,val,new_csp):
    new_csp.D[x] = [val]
    for k in neighboors(x,new_csp):
        if len(new_csp.D[k]) > 1: 
            new_csp.D[k] = [y for y in new_csp.D[k] if new_csp.C(val,x,y,k)]
    return ac3(new_csp)

def backtracking(csp1):
    print(csp1)
    if allSingle(csp1): return csp1
    if anyEmpty(csp1): return "Falha2"
    i = selectVar(csp1)
    for v in sortValues(i,csp1):
        csp2 = assign(i,v,csp(str(csp1)))
        if csp2: 
            sol = backtracking(csp(str(csp2)))
            if sol: return sol
    return None