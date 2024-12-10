#!python3

file = 'test.txt'
file = 'real.txt'

orig = [line.rstrip() for line in open(file)]

LEN=4

def get(x,y):
    if 0 <= x < len(orig) and 0 <= y < len(orig[0]):
        return orig[x][y]
    return ' '

def match(s):
    return s == "XMAS" or s == "SAMX"

def find():
    global orig
    total = 0

    for x in range(len(orig)):
        for y in range(len(orig)):
            if match("".join(get(x+i,y+i) for i in range(LEN))):
                total += 1
            if match("".join(get(x+LEN-1-i,y+i) for i in range(LEN))):
                total += 1
            if match("".join(get(x,y+i) for i in range(LEN))):
                total += 1
            if match("".join(get(x+i,y) for i in range(LEN))):
                total += 1
    return total

print("%d"%find())
