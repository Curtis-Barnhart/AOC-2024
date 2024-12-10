#!python3

file = 'test.txt'
file = 'real.txt'

orig = [line.rstrip() for line in open(file)]

def get(x,y):
    if 0 <= x < len(orig) and 0 <= y < len(orig[0]):
        return orig[x][y]
    return ' '

def match(s, a, b, c):
    return a+b+c == s or c+b+a == s

def find(s):
    global orig
    hits = set()

    for x in range(len(orig)):
        for y in range(len(orig)):
            if match(s, get(x,y), get(x+1,y+1), get(x+2,y+2)) and match(s, get(x+2,y), get(x+1,y+1), get(x,y+2)):
                hits.add((x+1,y+1))
    return hits

print("%d"%len(find("MAS")))
