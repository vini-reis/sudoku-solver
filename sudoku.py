import numpy as np
import math

possibilities = range(1,10)

class Board():
    def __init__(self, state : str):
        if len(state) != 81: pass
        self._flat = np.array([int(i) if i != '.' else 0 for i in state])
        self._rows = np.array([[int(state[i+j*9]) if state[i+j*9] != '.' else 0 for i in range(9)] for j in range(9)])
        self._cols = np.array([[self._rows[i][j] for i in range(9)] for j in range(9)])
        self._boxs = np.array([[self._rows[i+3*l][j+3*k] for i in range(3) for j in range(3)] for l in range(3) for k in range(3)])

    def __str__(self):
        return "".join(self._flat)

    def getRow(self, row : int) -> list or None:
        return self._rows[row] if row >= 0 and row < 9 else None

    def getColumn(self, col : int) -> list or None:
        return self._cols[col] if col >= 0 and col < 9 else None
    
    def getBox(self, box : int) -> list or None:
        return self._boxs[box] if box >= 0 and box < 9 else None

    def check(self, row : int = None, col : int = None, num : int = None) -> bool:
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
            if col is None:
                col = row % 9
                row = math.floor(row / 9)
            # Se já existe valor, o único valor válido é ele mesmo
            if self._rows[row][col] != 0: return self._rows[row][col] == num
            # Se não existe valor, checamos
            return num not in self._rows[row] and num not in self._cols[col] and num not in self._boxs[math.floor(row / 3) + math.floor(col / 3)*3]

    def goal(self) -> bool:
        if 0 in self._flat:
            return False
        return self.check()

class CSP(Board):
    def __init__(self, state: str):
        super().__init__(state)
        self.neighboors : list = [set([math.floor(i / 9) * 9 + k for k in range(9)] + [(i % 9) + 9 * k for k in range(9)] + [(j + 3 * math.floor((i % 9) / 3)) + (math.floor(i / 27) * 27 + k * 9) for k in range(3) for j in range(3)]) for i in range(81)]

        self.X : list = [True if self._flat[i] == 0 else False for i in range(81)]
        self.D : list = [[v for v in possibilities if self.check(c, num = v)] if self.X[c] else [self._flat[c]] for c in range(81)]
        self.C : list = [set([self._flat[e] for e in self.neighboors[c] if self._flat[e] != 0]) if self.X[c] else self._flat[c] for c in range(81)]

        self.queue = list(set((i, j) for i in range(81) for j in range(81) if self.X[i] and self.X[j] and i < j and i in self.neighboors[j]))

    def __str__(self):
        return "".join([str(self.D[c][0]) if not self.X[c] else '.' for c in range(81)])

    def valid(self):
        for c in range(81):
            if len(self.D[c]) == 0:
                return False
        return True

    def goal(self):
        for c in range(81):
            if len(self.D[c]) != 1:
                return False
        return True

    def update(self):
        self.X = [True if len(self.D[i]) != 1 else False for i in range(81)]
        self.C = [set([v for e in self.neighboors[c] for v in self.D[e]]) if self.X[c] else [v for v in possibilities if v != self.D[c][0]] for c in range(81)]
        self.D = [[v for v in self.D[c] if v not in self.C[c]] if self.X[c] else self.D[c] for c in range(81)]

def revise(csp : CSP, i : int, j : int):
    violate = [v for v in csp.D[i] if v in csp.C[j]]
    if len(violate) > 0:
        csp.D[i] = [i for i in csp.D[i] if i not in violate]
        csp.update()
        return True
    return False

def AC3(csp : CSP):
    if len(csp.queue) == 0: return True

    i,j = csp.queue.pop()
    if revise(csp, i, j):
        if len(csp.D[i]) == 0: return False
        [csp.queue.append((i,k)) for k in csp.neighboors[i] if k != i]
    return AC3(csp)

def selectVar(csp : CSP) -> int:
    count = [(len(csp.D[c]), c) for c in range(81) if csp.X[c]]
    return sorted(count, reverse=True)[0][1]

def sortValues(i : int, csp : CSP):
    count = [(len([True for k in range(81) if csp.X[i] and v in csp.D[k]]), v) for v in csp.D[i]]
    count = sorted(count)
    return [v[1] for v in count]

def assign(v, i, csp) -> CSP:
    csp.D[i] = [v]
    csp.update()
    return AC3(csp)

def backtracking(csp):
    print(csp)
    if csp.goal(): return csp
    # if not csp.valid(): return "Falha!"
    i = selectVar(csp)
    for v in sortValues(i, csp):
        if assign(v,i,csp):
            sol = backtracking(csp)
            if (sol): return sol
    return False