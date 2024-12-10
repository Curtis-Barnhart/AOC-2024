#!python3

import devin_filelib as fl

file = 'test.txt'
file = 'real.txt'

lines, rows, cols = fl.readLines(file)

def findNear(row, col, char):
    for dr, dc in [(1,0),(0,1),(-1,0),(0,-1)]:
        r = row+dr
        c = col+dc
        if 0 <= r < rows and 0 <= c < cols and lines[r][c] == char:
            yield (r,c)

def pathCount(points):
    for i in range(1,10):
        newPoints = set()
        for point in points:
            newPoints.update(findNear(*point, "%d"%i))
        points = newPoints
    return points

total = 0
for row1 in range(rows):
    for col1 in range(cols):
        if lines[row1][col1] == '0':
            score = len(pathCount([(row1, col1)]))
            total += score

print("total %d"%total)

