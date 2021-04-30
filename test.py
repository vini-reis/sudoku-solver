import sudoku as s

b = s.Board(".......2143.......6........2.15..........637...........68...4.....23........7....")
print("Rows:")
for i in range(9):
    print(b.getRow(i))

print("Cols:")
for i in range(9):
    print(b.getColumn(i))

print("Boxes:")
for i in range(9):
    print(b.getBox(i))