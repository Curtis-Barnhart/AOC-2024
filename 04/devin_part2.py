#!python3

file = 'test.txt'
file = 'real.txt'

orig = [line.rstrip() for line in open(file)]
x=orig

def check():
    global x,hits

    print("-----")
    print("\n".join(x))

    ln = 0
    for a in x:
        i=0
        try:
            while True:
                i = a.index("MAS", i) + 1

                x=ln
                y=i
                xx=x+y-len(orig)
                print("MAS (%d,%d) -> (%d,%d)"%(x,y,xx,y))

                hits.add((xx,y))
        except Exception:
            pass
        i=0
        try:
            while True:
                i = a.index("SAM", i) + 1

                x=ln
                y=i
                xx=x+y-len(orig)
                print("SAM (%d,%d) -> (%d,%d)"%(x,y,xx,y))

                hits.add((xx,y))
        except Exception:
            pass
        ln += 1
            
x=[]
hits = set()
for j in range(len(orig[0]), 0, -1):
    x.append(" "*j + "".join([orig[i][j+i] for i in range(len(orig)-j)]))
for j in range(0, len(orig[0])):
    x.append("".join([orig[j+i][i] for i in range(len(orig)-j)]))
check()
hits1 = hits
print(repr(hits1))

x=[]
hits = set()
for j in range(len(orig[0]), 0, -1):
    x.append(" "*j + "".join([orig[len(orig)-1-(i)][j+i] for i in range(len(orig)-j)]))
for j in range(0, len(orig[0])):
    x.append("".join([orig[len(orig)-1-(j+i)][i] for i in range(len(orig)-j)]))
check()
hits2 = set((len(orig)-1-x,y) for x,y in hits)

isec = hits1.intersection(hits2)
print(repr(hits2))

print(repr(isec))
print("t %d"%len(hits1.intersection(hits2)))
