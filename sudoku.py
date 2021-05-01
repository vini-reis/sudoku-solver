from typing import Union
import numpy as np
import math

class Board():
    def __init__(self, state : str):
        if len(state) != 81: pass
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

    def check(self, row=None, col=None, num=None) -> bool:
        if row is None:
            for r in self._rows:
                v = set()
                for i in r:
                    if i not in v: 
                        v.add(i)
                    else: 
                        return False
            for c in self._cols:
                v = set()
                for i in c:
                    if i not in v:
                        v.add(i)
                    else:
                        return False
            for b in self._boxs:
                v = set()
                for i in b:
                    if i not in v:
                        v.add(i)
                    else:
                        return False
            return True
        else:
            # Se já existe valor, o único valor válido é ele mesmo
            if self._rows[row][col] != 0: return self._rows[row][col] == num
            # Se não existe valor, checamos
            return num not in self._rows[row] and num not in self._cols[col] and num not in self._boxs[math.floor(row / 3) + math.floor(col / 3)*3]

    def goal(self) -> bool:
        if 0 in self._rows.flatten():
            return False
        return self.check()

class CSP(Board):
    def __init__(self, state: str):
        super().__init__(state)
        self.X = range(1,10)
        self.D = np.array([[np.array([num for num in self.X if self.check(row,col,num)]) for row in range(9)] for col in range(9)])
        self.C = np.array([[set(self._rows[row] + self._cols[col] + self._boxs[math.floor(row / 3) + math.floor(col / 3)*3] - [0]) for row in range(9)] for col in range(9)])

        self.queue = [(row, col) for row in range(9) for col in range(9) if len(self.D[row][col]) > 1]

    def __str__(self):
        return "".join([str(self.D[row][col]) if len(self.D[row][col]) == 1 else str(0) for row in range(9) for col in range(9)])

    def valid(self):
        for row in range(9):
            for col in range(9):
                if len(self.D[row][col]) == 0:
                    return False
        return True

    def goal(self):
        for row in range(9):
            for col in range(9):
                if len(self.D[row][col]) != 1:
                    return False
        return True

    def neighboors(self,r,c):
        return [(i, j) for i in range(9) for j in range(9) if i == r or j == c or math.floor(i/3) == math.floor(r/3) or math.floor(j/3) == math.floor(c/3)]

    def updateC(self):
        self.C = np.array([[set(self._rows[row] + self._cols[col] + self._boxs[math.floor(row / 3) + math.floor(col / 3)*3] - [0]) for row in range(9)] for col in range(9)])

def revise(csp : CSP, i : int, j : int):
    violate = np.array([v for v in csp.D[i][j] if v in csp.C[i][j]])
    if violate.any():
        csp.D[i][j] = [i for i in csp.D[i][j] if i not in violate]
        csp.updateC()
        return True
    return False

def AC3(csp):
    print(csp)
    if not len(csp.queue) > 0: return True
    if csp.goal(): return str(csp)

    i,j = csp.queue.pop()
    if revise(csp, i, j):
        if len(csp.D[i][j]) == 0: return False
        [csp.queue.append((a,b)) for a,b in csp.neighboors(i,j) if i != a and j != b]
    return AC3(csp)
