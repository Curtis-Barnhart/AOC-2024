#!python3

import sys

file = 'test.txt'
file = 'real.txt'

lines = [line.rstrip() for line in open(file)]


up = {}
down = {}

def addin(m,k,v):
    if k in m:
        m[k].add(v)
    else:
        m[k]=set([v])

x = []

first = True
for line in lines:
    if not line:
        first = False
        continue
    if first:
        splt=line.split("|")
        s0 = splt[0]
        s1 = splt[1]

        addin(up, s0, s1)
        addin(down, s1, s0)
    else:
        x.append(line.split(","))

print(repr(up))
print(repr(down))
def compX(a,b):
    if a in up:
        if b in up[a]:
            return -1
    if a in down:
        if b in down[a]:
            return 1
    if b in up:
        if a in up[b]:
            return 1
    if b in down:
        if a in down[b]:
            return -1
    return 0

def sortIt(l):
    ll = []
    for lll in l:
        for i in range(len(ll)):
            if compX(ll[i], lll) == 1:
                ll.insert(i,lll)
                break
        else:
            ll.append(lll)
    return ll

t=0
for xx in x:
    yy = sortIt(xx)
    print("... %s %s"%(xx,yy))
    if xx != yy:
        print("good %s"%repr(xx))
        t += int(yy[len(yy)//2])

print("%d"%t)
