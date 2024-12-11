#!python3

import sys

import devin_listlib as ll

file = 'test.txt'
file = 'real.txt'

def transform(i):
    if i == 0:
        return (1,)
    else:
        s = "%d"%i
        l = len(s)
        if l%2 == 0:
            h = l//2
            return (int(s[:h]), int(s[h:]))
        else:
            return (i*2024,)

with open(file) as fh:
    stList = ll.StackedTransformList([int(i) for i in fh.read().rstrip().split(" ")])

for i in range(75):
    stList.addTransform(transform)

print("%d"%(stList.getLen()))

