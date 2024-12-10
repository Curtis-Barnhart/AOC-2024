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

def pathCount(row, col, char):
    if char == '10':
        return 1
    return sum(pathCount(*fork, "%d"%(int(char)+1)) for fork in findNear(row, col, char))

def endCount(points):
    for i in range(1,10):
        newPoints = set()
        for point in points:
            newPoints.update(findNear(*point, "%d"%i))
        points = newPoints
    return len(points)

part1 = 0
part2 = 0
for row1 in range(rows):
    for col1 in range(cols):
        if lines[row1][col1] == '0':
            part1 += endCount([(row1, col1)])
            part2 += pathCount(row1, col1, '1')

print("part1 %d part2 %d"%(part1, part2))

