#!python3

import sys

file = 'test.txt'
file = 'real.txt'

def readFile():
    global lines, rows, cols

    lines = [list(line.rstrip()) for line in open(file)]
    rows = len(lines)
    cols = len(lines[0])

def findStart():
    global rowX, colX
    rowX = 0
    for line in lines:
        if "^" in line:
            break
        rowX += 1
    colX = line.index("^")

def trace():
    global lines, rows, cols, rowX, colX

    row = rowX
    col = colX

    dRow = -1
    dCol = 0

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

            dRow2 = dCol
            dCol2 = -dRow

            dRow = dRow2
            dCol = dCol2
        elif val != "#" and val != "X":
            lines[row][col] = "X"
            total += 1
        else:
            row += dRow
            col += dCol

            if not (0 <= row < rows) or not (0 <= col < cols):
                return (False, total)

readFile()
findStart()

t2 = 0
for i in range(rows):
    for j in range(cols):
        readFile()
        if lines[i][j] == ".":
            lines[i][j] = "#"
        status, total = trace()
        if status:
            t2 += 1

print("t2 %d"%t2)
