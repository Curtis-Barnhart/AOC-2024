#!python3

import devin_maplib as ml

file = 'test.txt'
file = 'real.txt'

m = ml.CharMap(file)

antenna = m.getPoints("0-9a-zA-Z")

rows = m.rows
cols = m.cols

spots = set()
for k,v in antenna.items():
    v = list(v)
    for i in range(len(v)):
        for j in range(i+1, len(v)):
            r1,c1 = v[i]
            r2,c2 = v[j]

            dRow = r2-r1
            dCol = c2-c1

            r = r1 - dRow
            c = c1 - dCol
            if m.validPoint(r,c):
                spots.add((r,c))

            r = r2 + dRow
            c = c2 + dCol
            if m.validPoint(r,c):
                spots.add((r,c))

print("points %d"%(len(spots)))
