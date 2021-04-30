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

    def check(self, row, col, num):
        # Se já existe valor, o único valor válido é ele mesmo
        if self._rows[row][col] != 0: return self._rows[row][col] == num
        # Se não existe valor, checamos
        return num not in self._rows[row] & num not in self._cols[col] & num not in self._boxs[math.floor(row / 3) + math.floor(col)*3]

    def goal(self) -> bool:
        if 0 in self._rows.flatten():
            return False
        return self.check()

class CSP():
    def __init__(self, b : Board):
        self.X = range(1,10)
        self.D = [[[num for num in self.X if b.check(row,col,num)] for row in range(9)] for col in range(9)]
        self.C = [[[num for num in self.X if num not in self.D] for row in range(9)] for col in range(9)]

        self.queue = [(row,col) for row in range(9) for col in range(9) if len(self.D[row][col]) > 1]