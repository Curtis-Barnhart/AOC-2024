#!python3

import devin_maplib as ml

file = 'test.txt'
file = 'real.txt'

m = ml.CharMap(file)

antenna = m.getPoints("0-9a-zA-Z")

rows = m.rows
cols = m.cols

def drawLine(r1, c1, r2, c2):
    global spots

    dRow = r2-r1
    dCol = c2-c1

    for p in range(2,1+max(dRow, dCol)):
        while p*(dRow // p) == dRow and p*(dCol // p) == dCol:
            dRow //= p
            dCol //= p
    r = r1
    c = c1
    while m.validPoint(r,c):
        spots.add((r,c))
        r += dRow
        c += dCol
    r = r1
    c = c1
    while m.validPoint(r,c):
        spots.add((r,c))
        r -= dRow
        c -= dCol

spots = set()
for k,v in antenna.items():
    v = list(v)
    for i in range(len(v)):
        for j in range(i+1, len(v)):
            r1,c1 = v[i]
            r2,c2 = v[j]

            drawLine(r1,c1,r2,c2)


print("points %d"%(len(spots)))
