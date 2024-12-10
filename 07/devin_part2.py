#!python3

file = 'test.txt'
file = 'real.txt'

def readFile(file):
    global lines

    lines = [line.rstrip() for line in open(file)]


readFile(file)
xx = [[int(x.replace(":","")) for x in parts] for parts in [line.split(" ") for line in lines]]

def solvable(lst, total, i):
    if i == len(lst):
        return total == lst[0]
    nxt = lst[i]
    if solvable(lst, total+nxt, i+1):
        return True
    if solvable(lst, total*nxt, i+1):
        return True
    if solvable(lst, int("%d%d"%(total,nxt)), i+1):
        return True

total = 0
for x in xx:
    if solvable(x, x[1], 2):
        total += x[0]

print("%d"%total)
