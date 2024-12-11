#!python3

file = 'test.txt'
file = 'real.txt'

ints1 = [[int(i)] for i in open(file).read().rstrip().split(" ")]

def blink():
    for idx1 in range(len(ints1)):
        ints2 = ints1[idx1]
        updates = []
        for idx2 in range(len(ints2)):
            i = ints2[idx2]

            if i == 0:
                ints2[idx2] = 1
            else:
                s = "%d"%i
                l = len(s)
                if l%2 == 0:
                    h = l//2
                    ints2[idx2] = int(s[h:])
                    updates.append((idx2, int(s[:h])))
                else:
                    ints2[idx2] = i*2024
        updates.reverse()
        for idx, val in updates:
            ints2.insert(idx,val)

def prt():
    return " ".join(str(i) for ints2 in ints1 for i in ints2)

for i in range(75):
    blink()

print("%d"%(sum(len(ints2) for ints2 in ints1)))
