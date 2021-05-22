import numpy as np
import math
import progressbar

possibilities = range(1,10)

class Board():
    def __init__(self, state : str):
        if len(state) != 81: pass
        self._flat = np.array([int(i) if i != '.' else 0 for i in state])
        self._rows = np.array([[int(state[i+j*9]) if state[i+j*9] != '.' else 0 for i in range(9)] for j in range(9)])
        self._cols = np.array([[self._rows[i][j] for i in range(9)] for j in range(9)])
        self._boxs = np.array([[self._rows[i+3*l][j+3*k] for i in range(3) for j in range(3)] for l in range(3) for k in range(3)])

        self.neighboors : list = [set([math.floor(i / 9) * 9 + k for k in range(9)] + [(i % 9) + 9 * k for k in range(9)] + [(j + 3 * math.floor((i % 9) / 3)) + (math.floor(i / 27) * 27 + k * 9) for k in range(3) for j in range(3)]) for i in range(81)]

    def __str__(self):
        return "".join(self._flat)

    def check(self) -> bool:
        for r in self._rows:
            v = set()
            for i in r:
                if i not in v and i != 0:
                    v.add(i)
                elif i != 0:
                    return False
        for c in self._cols:
            v = set()
            for i in c:
                if i not in v and i != 0:
                    v.add(i)
                elif i != 0:
                    return False
        for b in self._boxs:
            v = set()
            for i in b:
                if i not in v and i != 0:
                    v.add(i)
                elif i != 0:
                    return False
        return True

    def goal(self) -> bool:
        if 0 in self._flat:
            return False
        return self.check()

    def print(self):
        print()
        for i,r in enumerate(self._rows):
            if i % 3 == 0 and i > 0: 
                print('|---+---+---|')
            for j,c in enumerate(r):
                if j % 3 == 0:
                    print('|', end='')
                print(c,end='')
            print('|')
        print()

class CSP(Board):
    def __init__(self, state: str):
        super().__init__(state)

        self.X : list = [i for i in range(81) if self._flat[i] == 0]
        self.C : list = [set([self._flat[e] for e in self.neighboors[c] if e not in self.X]) if c in self.X else [p for p in possibilities if p != self._flat[c]] for c in range(81)]
        self.D : list = [[v for v in possibilities if v not in self.C[c]] if c in self.X else [self._flat[c]] for c in range(81)]
        self.X = [x for x in self.X if len(self.D[x]) > 1]
        self._flat = np.array([self.D[c][0] if len(self.D[c]) == 1 else 0 for c in range(81)])

    def __str__(self):
        return "".join([str(self.D[c][0]) if len(self.D[c]) == 1 else '.' for c in range(81)])

    def valid(self):
        for c in range(81):
            if len(self.D[c]) == 0:
                return False
        return True

    def goal(self):
        for c in range(81):
            if len(self.D[c]) != 1:
                return False
            elif self.D[c][0] in self.C[c]:
                return False
        return True

    def update(self, i : int or None = None):
        # FIXME: Check corretude of updated CSP
        # rng = self.neighboors[i] if i is not None else range(81)
        rng = range(81)
        if i is not None and i in self.X: self.X.remove(i);
        self.C = [set([self.D[e][0] for e in self.neighboors[c] if e not in self.X]) if c in self.X else set([p for p in possibilities if p not in self.D[c]]) for c in range(81)]
        self.D = [[v for v in self.D[c] if v not in self.C[c]] if c in self.X else self.D[c] for c in range(81)]
        self.X = [x for x in self.X if len(self.D[x]) > 1]
        self._flat = np.array([self.D[c][0] if len(self.D[c]) == 1 else 0 for c in range(81)])

    def test(self, i : int, vi : int, vj : int):
        test_set : set = {vi}
        for n in self.neighboors[i]:
            test_set.union(self.D[n])
        return not vj in test_set

    def queue(self):
        return list(set((i, j) for i in range(81) for j in range(81) if i in self.X and j in self.X and i < j and i in self.neighboors[j]))

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

def selectVar(csp : CSP) -> int:
    count = [(len(csp.C[c]), c) for c in csp.X]
    return sorted(count, reverse=True)[0][1]

def sortValues(i : int, csp : CSP):
    count = [(len([True for k in csp.neighboors[i] if v in csp.D[k] and k in csp.X]), v) for v in csp.D[i]]
    count = sorted(count, reverse=True)
    return [v[1] for v in count]

def assign(v, i, csp : CSP):
    csp_novo : CSP = CSP(str(csp))
    csp_novo.D[i] = [v]
    if csp_novo.valid() and csp_novo.check():
        csp_novo.update(i)
        csp = csp_novo
        return True, csp
        return AC3(csp, csp.queue())
    return False, csp

def backtracking(csp : CSP):
    print(csp, csp.check())
    if csp.goal(): return csp
    if not csp.valid(): return False
    i = selectVar(csp)
    for v in csp.D[i]:
        sol : CSP or bool = assign(v,i,CSP(str(csp)))
        if sol and sol.valid() and sol.check():
            sol = backtracking(sol)
            if sol: return sol
    return False

def pureBack(csp : CSP):
    print(csp)
    if len(csp.X) == 0: return csp

    i = selectVar(csp)
    for v in csp.D[i]:
        consistent, csp = assign(v, i, csp)
        if consistent:
            sol = pureBack(csp)
            if sol: return sol
    return False
