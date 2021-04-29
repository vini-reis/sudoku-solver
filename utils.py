# Constants
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