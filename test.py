import sudoku as s

c = s.CSP(".......2143.......6........2.15..........637...........68...4.....23........7....")
print(s.backtracking(c))