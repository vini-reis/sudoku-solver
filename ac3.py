from utils import *

def constraints(board):
    constraints = [(k+j*9,j*9+i) for k in range(9) for j in range(9) for i in range(9) if k != i] # Tuplas das linhas
    constraints.extend([(j+9*i,j+9*k) for i in range(9) for j in range(9) for k in range(9)])
    constraints.extend([(n*9+l*3+m+27*i,27*i+l*3+9*k+j) for i in range(3)
                                          for n in range(3)
                                          for l in range(3)
                                          for m in range(3)
                                          for k in range(3)
                                          for j in range(3)
                                          if n*9+l*3+m+27*i != 27*i+l*3+9*k+j])
    return set([(x,y) for x,y in constraints if x != y])

def worklist(csp1):
    return set([(x,y) for x,y in constraints(str(csp1)) if str(csp1)[x] == '.' or str(csp1)[y] == '.'])

class csp(object):
    def __init__(self,board):
        self.X = [i for i in range(len(board)) if board[i] == '.']
        self.D = [[str(x) for x in possibilities if is_valid(strrplchar(board,str(x),y))] if board[y] == '.' else [board[y]] for y in range(len(board))]
        self.C = lambda x,i,y,j : is_valid(strrplchar(strrplchar(self.answer(),x,i),y,j))

    def answer(self):
        return "".join([self.D[i][0] if len(self.D[i]) == 1 else '.' for i in range(len(self.D))])

    def __str__(self):
        return "".join([self.D[i][0] if len(self.D[i]) == 1 else '.' for i in range(len(self.D))])

def neighboors(i, csp1):
    return set([y for x,y in constraints(str(csp1)) if (x == i)])

def revise(csp1, i, j):
    D = csp1.D
    violate = set([x for x in D[i] if True not in [csp1.C(x,i,y,j) for y in D[j]]])
    if len(violate) > 0:
        csp1.D[i] = [x for x in D[i] if x not in violate]
        return True, csp1
    return False, csp1

def ac3(csp1):
    queue = worklist(csp1)
    while queue:
        i, j = queue.pop()
        revised, csp1 = revise(csp1, i, j)
        if revised:
            D = csp1.D
            if len(D[i]) == 0: return None
            temp = [x for x in queue]
            neighboors_list = neighboors(i,csp1)
            temp.extend([(k,i) for k in neighboors_list if (k,i) not in queue])
            queue = set(temp)
    return csp1