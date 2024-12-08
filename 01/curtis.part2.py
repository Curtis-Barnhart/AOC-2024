import sys
from collections import Counter

if __name__ == "__main__":
    llist, rlist = [], []
    for line in open(sys.argv[1], "r"):
        numbers = line.split("   ")
        llist.append(int(numbers[0]))
        rlist.append(int(numbers[1]))

    rcnt = Counter(rlist)

    solution = sum((value * rcnt[value] for value in llist))
    print("Solution: {:d}!".format(solution))

