#!python3

file = 'test.txt'
file = 'real.txt'

def readFile():
    # mutable
    global lines, rows, cols

    lines = [list(line.rstrip()) for line in open(file)]
    rows = len(lines)
    cols = len(lines[0])

def findStart():
    # mutable
    global rowX, colX

    # immutable
    global lines

    rowX = 0
    for line in lines:
        if "^" in line:
            break
        rowX += 1
    colX = line.index("^")

def trace(markup):
    # mutable
    global lines

    # immutable
    global rows, cols, rowX, colX

    row, col = rowX, colX
    dRow, dCol = -1, 0

    total = 0
    walked = set()

    while True:
        val = lines[row][col]
        if val == "#":
            row -= dRow
            col -= dCol

            step = (row, col, dRow, dCol)
            if step in walked:
                return (True, total)
            walked.add(step)

            dRow, dCol = dCol, -dRow
        elif markup and val != "#" and val != "X":
            lines[row][col] = "X"
            total += 1
        else:
            row += dRow
            col += dCol

            if not (0 <= row < rows) or not (0 <= col < cols):
                return (False, total)

readFile()
findStart()
status, steps = trace(True)

blocks = 0
for i in range(rows):
    for j in range(cols):
        if lines[i][j] == "X":
            lines[i][j] = "#"
            status, total = trace(False)
            if status:
                blocks += 1
            lines[i][j] = "X"

print("%d steps and %d possible blocks"%(steps, blocks))

