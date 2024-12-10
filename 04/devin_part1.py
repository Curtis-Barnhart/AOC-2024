#!python3

file = 'test.txt'
file = 'real.txt'

orig = [line.rstrip() for line in open(file)]
x=orig

t = 0

def check():
    global x,t

#    print("-----")
#    print("\n".join(x))
    for a in x:
        i=0
        try:
            while True:
                i = a.index("XMAS", i) + 4
                t += 1
        except Exception:
            pass
        i=0
        try:
            while True:
                i = a.index("SAMX", i) + 4
                t += 1
        except Exception:
            pass
#    print("ttt %d"%t)
            

# don't rotate
check()

# rotate 90
x=[]
for j in range(len(orig[0])):
    x.append("".join([orig[i][j]for i in range(len(orig))]))
check()

# rotate 45 (kinda)
x=[]
for j in range(len(orig[0]), 0, -1):
    x.append("".join([orig[i][j+i] for i in range(len(orig)-j)]))
for j in range(0, len(orig[0])):
    x.append("".join([orig[j+i][i] for i in range(len(orig)-j)]))
check()

# rotate -45 (kinda)
x=[]
for j in range(len(orig[0]), 0, -1):
    x.append("".join([orig[len(orig)-1-(i)][j+i] for i in range(len(orig)-j)]))
for j in range(0, len(orig[0])):
    x.append("".join([orig[len(orig)-1-(j+i)][i] for i in range(len(orig)-j)]))
check()

print("t %d"%t)
