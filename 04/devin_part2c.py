#!python3

file = 'test.txt'
file = 'real.txt'

orig = [line.rstrip() for line in open(file)]

LEN=3

def get(x,y):
    if 0 <= x < len(orig) and 0 <= y < len(orig[0]):
        return orig[x][y]
    return ' '

def match(s):
    return s == "MAS" or s == "SAM"

def find():
    global orig
    hits = set()

    for x in range(len(orig)):
        for y in range(len(orig)):
            if match("".join(get(x+i,y+i) for i in range(LEN))) and match("".join(get(x+LEN-1-i,y+i) for i in range(LEN))):
                hits.add((x+1,y+1))
    return hits

print("%d"%len(find()))
