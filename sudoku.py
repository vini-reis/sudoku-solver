import sys

# CONSTANT
possibilities = [str(i) for i in range(1,10)]

def read_board(filename):
    with open(filename,'r') as file:
        boards = file.readlines()
        for i in range(len(boards)):
            boards[i] = boards[i][:81]
        return boards

def lines(board):
    return [board[9*i:9*(i+1)] for i in range(9)]

def columns(board):
    return ["".join([board[(9*j)+i] for j in range(9)]) for i in range(9)]

def boxes(board):
    return ["".join([lines(board)[(i*3)+k][3*j:3*(j+1)] for k in range(3)])
                                                       for i in range(3)
                                                       for j in range(3)]

def print_board(board):
    lines = lines(board)
    for i in range(9):
        print('|',lines[i][:3],'|',lines[i][3:6],'|',lines[i][6:],'|',sep="")
        if (i+1) % 3 == 0 and i < 8: print("|---+---+---|")
    print("")

def no_dups(board):
    verif = set()
    for cell in board:
        if cell not in verif and cell != '.':
            verif.add(cell)
        elif cell in verif:
            return False
    return True

def is_valid(board):
    for s in lines(board):
        if not no_dups(s): return False
    for s in columns(board):
        if not no_dups(s): return False
    for s in boxes(board):
        if not no_dups(s): return False
    return True

def strrplchar(str,carac,index):
    return (str[:index] + carac + str[index+1:])

def expand(board):
    return [strrplchar(board,n,board.find('.')) for n in possibilities if is_valid(strrplchar(board,n,board.find('.')))]

def goal_reached(board):
    return ('.' not in board) & is_valid(board)

def cost(board):
    return board.count('.')

def g(board):
    return len(board) - board.count('.')

def h1(board):
    # Heurística 1: soma da quantidade de possibilidades de cada célula do boarduleiro
    h = 0
    for i in range(len(board)):
        if board[i] == '.':
            for p in possibilities:
                if is_valid(strrplchar(board,p,i)):
                    h+=1
    return h

def bfs(board):
    visitados = set()
    fila = [board,]

    while fila:
        s = fila.pop(0)
        if s not in visitados and is_valid(s):
            if goal_reached(s):
                return s
            visitados.add(s)
            # print(s) #debug
            fila.extend(expand(s))
            fila.sort(key=cost)

def dfs(board):
    visited = set()
    visited.add(board)
    if goal_reached(board): return board
    queue = [board]
    while queue:
        state = queue.pop()
        for s in expand(state):
            if s not in visited and is_valid(s):
                # print(s) #debug
                if goal_reached(s): return s
                visited.add(s)
                queue.append(s)
    return None

def greedy(board,h):
    visited = set()
    nodes = expand(board)

    while nodes:
        node = min(nodes,key=h)
        if node not in visited and is_valid(node):
            sl = expand(node)
            # print(node) #debug
            for a in sl:
                if goal_reached(a): return a
        visited.add(node)
        nodes.remove(node)
        nodes.extend(sl)

def astar(board,g,h):
    visited = set()
    nodes = expand(board)

    while nodes:
        node = min(nodes,key=lambda a : g(a)+h(a))
        if node not in visited and is_valid(node):
            sl = expand(node)
            # print(node) #debug
            for a in sl:
                if goal_reached(a): return a
        visited.add(node)
        nodes.remove(node)
        nodes.extend(sl)

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
    if allSingle(csp1): return csp1
    if anyEmpty(csp1): return "Falha2"
    i = selectVar(csp1)
    for v in sortValues(i,csp1):
        csp2 = assign(i,v,csp(str(csp1)))
        if csp2: 
            sol = backtracking(csp(str(csp2)))
            if sol: return sol
    return None

# Lendo argumentos:
filename = sys.argv[1]
algorithm = sys.argv[2]

if algorithm == "bfs":
    for board in read_board(filename):
        print(bfs(board))
elif algorithm == "dfs":
    for board in read_board(filename):
        print(dfs(board))
elif algorithm == "greedy":
    for board in read_board(filename):
        print(greedy(board,h1))
elif algorithm == "astar":
    for board in read_board(filename):
        print(astar(board,g,h1))
elif algorithm == "ac3":
    for board in read_board(filename):
        print(ac3(csp(board),worklist(board)))
elif algorithm == "backtracking":
    for board in read_board(filename):
        print(backtracking(csp(board)))
