from ac3 import neighboors
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

        self.X : list = [i for i in range(81) if self._flat[i] == 0]
        self.D : list = [[v for v in possibilities if self.check(c, num = v)] if c in self.X else [self._flat[c]] for c in range(81)]
        self.C : list = [set([self._flat[e] for e in self.neighboors[c] if e not in self.X]) if c in self.X else [p for p in possibilities if p != self._flat[c]] for c in range(81)]

        self.queue = list(set((i, j) for i in range(81) for j in range(81) if i in self.X and j in self.X and i < j and i in self.neighboors[j]))

    def __str__(self):
        return "".join([str(self.D[c][0]) if c not in self.X else '.' for c in range(81)])

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

    def update(self, i : int):
        self.X.remove(i)
        self.C = [set([v for e in self.neighboors[c] for v in self.D[e] if e not in self.X]) if c not in self.X else [v for v in possibilities if v != self.D[c][0]] for c in range(81)]
        self.D = [[v for v in self.D[c] if v not in self.C[c]] if c in self.X else self.D[c] for c in range(81)]

    def test(self, i, vi, j, vj):
        # TODO: Otimizar o teste da revisão
        temp = {n for n in self.neighboors[i] if not self.X[n]}
        return vi not in set(self.D[k] for k in self.neighboors[i] if self.X[k]) and vj not in self.neighboors[j]

def revise(csp : CSP, i : int, j : int):
    violate = [vi for vi in csp.D[i] if True not in [csp.test(i, vi, j, vj) for vj in csp.D[j]]]
    if len(violate) > 0:
        csp.D[i] = [v for v in csp.D[i] if v not in violate]
        csp.update()
        return True
    return False

def AC3(csp : CSP):
    if len(csp.queue) == 0: return csp
    # print(csp)
    # print(len(csp.queue))

    i,j = csp.queue.pop()
    if revise(csp, i, j):
        if len(csp.D[i]) == 0: return False
        [csp.queue.append((k,i)) for k in csp.neighboors[i] if k != i and (k,i) not in csp.queue]
        csp.update()
        print("Revised!")
    return AC3(csp)

def selectVar(csp : CSP) -> int:
    count = [(len(csp.D[c]), c) for c in range(81) if csp.X[c]]
    return sorted(count, reverse=True)[0][1]

def sortValues(i : int, csp : CSP):
    count = [(len([True for k in range(81) if csp.X[i] and v in csp.D[k]]), v) for v in csp.D[i]]
    count = sorted(count)
    return [v[1] for v in count]

def assign(v, i, csp) -> CSP:
    csp2 : CSP = CSP(str(csp))
    csp2.D[i] = [v]
    csp2.update()
    return AC3(csp2)

def backtracking(csp : CSP):
    print(csp)
    csp.update()
    if csp.goal(): return csp
    if not csp.valid(): return "Falha!"
    i = selectVar(csp)
    for v in sortValues(i, csp):
        sol : CSP or bool = assign(v,i,csp)
        if sol:
            sol = backtracking(sol)
            if sol: return sol
    return False