#!python3

import sys

file = 'test.txt'
file = 'real.txt'

class LLN(object):
    def __init__(self, value, rest=None, newNode=False):
        if not newNode:
            self.value = value[0]
            self.rest = LLN(value[1:]) if len(value) > 1 else None
        else:
            self.value = value
            self.rest = rest

    def toList(self, lst):
        lst.append(self.value)
        if self.rest:
            self.rest.toList(lst)

    def replace(self, v1, v2):
        self.value = v1
        self.rest = LLN(v2, self.rest, True)
        return self.rest

    def getLen(self):
        ln = 1
        current = self.rest
        while current:
            ln += 1
            current = current.rest
        return ln

ints = LLN([int(i) for i in open(file).read().rstrip().split(" ")])

def blink():
    current = ints
    while current:
        i = current.value

        if i == 0:
            current.value = 1
        else:
            s = "%d"%i
            l = len(s)
            if l%2 == 0:
                h = l//2
                current = current.replace(int(s[:h]), int(s[h:]))
            else:
                current.value = i*2024
        current = current.rest

def prt():
    l=[]
    ints.toList(l)
    return " ".join(str(i) for i in l)

for i in range(75):
    blink()
    print("part %d"%i)

print("%d"%(ints.getLen()))
