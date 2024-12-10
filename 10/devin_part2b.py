#!python3

import devin_maplib as ml

file = 'test.txt'
file = 'real.txt'

m = ml.CharMap(file)
m.setNearDirs(4)

path="0123456789"

print("part1 %d part2 %d"%(m.endCount(path), m.pathCount(path)))

