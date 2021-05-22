import numpy as np
import math

possibilities = range(1,10)

class Board():
    def __init__(self, state : str):
        if len(state) != 81: pass
        self.board = np.array([int(i) if i != '.' else 0 for i in state])
        self.rows = np.array([[int(state[i+j*9]) if state[i+j*9] != '.' else 0 for i in range(9)] for j in range(9)])
        self.cols = np.array([[self.rows[i][j] for i in range(9)] for j in range(9)])
        self.boxs = np.array([[self.rows[i+3*l][j+3*k] for i in range(3) for j in range(3)] for l in range(3) for k in range(3)])

        self.neighboors = [set([math.floor(i / 9) * 9 + k for k in range(9)] + [(i % 9) + 9 * k for k in range(9)] + [(j + 3 * math.floor((i % 9) / 3)) + (math.floor(i / 27) * 27 + k * 9) for k in range(3) for j in range(3)]) for i in range(81)]

    def __str__(self):
        return "".join([str(c) if c != 0 else '.' for c in self.board])

    def check(self) -> bool:
        for r in self.rows:
            v = set()
            for i in r:
                if i not in v and i != 0:
                    v.add(i)
                elif i != 0:
                    return False
        for c in self.cols:
            v = set()
            for i in c:
                if i not in v and i != 0:
                    v.add(i)
                elif i != 0:
                    return False
        for b in self.boxs:
            v = set()
            for i in b:
                if i not in v and i != 0:
                    v.add(i)
                elif i != 0:
                    return False
        return True

    def goal(self) -> bool:
        if 0 in self.board:
            return False
        return self.check()

    def print(self):
        print()
        for i in range(81):
            if i % 3 == 0:
                print('| ', end='')
            if i % 9 == 0 and i > 0:
                print('')
                print('| ', end='')
            if i % 27 == 0 and i > 0: 
                print('------+-------+-------|')
                print('| ', end='')
            print(self.board[i],end=' ')
        print('|')

class CSP(Board):
    def __init__(self, state: str):
        super().__init__(state)

        self.C : list = [set([self.board[e] for e in self.neighboors[c] if self.board[e] != 0]) if self.board[c] == 0 else [p for p in possibilities if p != self.board[c]] for c in range(81)]
        self.D : list = [[v for v in possibilities if v not in self.C[c]] if self.board[c] == 0 else [self.board[c]] for c in range(81)]
        self.X : list = [x for x in range(81) if len(self.D[x]) > 1]
        self.board = np.array([self.D[c][0] if len(self.D[c]) == 1 else 0 for c in range(81)])
        self.rows = np.array([[int(self.board[i+j*9]) if self.board[i+j*9] != '.' else 0 for i in range(9)] for j in range(9)])
        self.cols = np.array([[self.rows[i][j] for i in range(9)] for j in range(9)])
        self.boxs = np.array([[self.rows[i+3*l][j+3*k] for i in range(3) for j in range(3)] for l in range(3) for k in range(3)])

    def __eq__(self, csp: object) -> bool:
        return [i for i, j in zip(self.board, csp.board) if i == j][0] == 81

    def valid(self):
        for c in range(81):
            if len(self.D[c]) == 0:
                return False
        return True

    def goal(self):
        if self.valid():
            for c in range(81):
                if self.D[c][0] in self.C[c]:
                    return False
            return self.check()
        return False

    def update(self, i : int):
        if i in self.X: self.X.remove(i)
        self.C = [set([self.D[e][0] for e in self.neighboors[c] if e not in self.X]) if c in self.X else set([p for p in possibilities if p not in self.D[c]]) for c in range(81)]
        self.D = [[v for v in possibilities if v not in self.C[c]] if c in self.X else self.D[c] for c in range(81)]
        self.X = [x for x in self.X if len(self.D[x]) > 1]
        self.board = np.array([self.D[c][0] if len(self.D[c]) == 1 else 0 for c in range(81)])
        self.rows = np.array([[int(self.board[i+j*9]) if self.board[i+j*9] != '.' else 0 for i in range(9)] for j in range(9)])
        self.cols = np.array([[self.rows[i][j] for i in range(9)] for j in range(9)])
        self.boxs = np.array([[self.rows[i+3*l][j+3*k] for i in range(3) for j in range(3)] for l in range(3) for k in range(3)])

    def test(self, i : int, vi : int, vj : int):
        test_set : set = {vi}
        for n in self.neighboors[i]:
            if n not in self.X:
                test_set.union(self.D[n])
        return not vj in test_set

    def queue(self):
        return list(set((i, j) for i in range(81) for j in range(81) if i in self.X and j in self.X and i < j and i in self.neighboors[j]))
