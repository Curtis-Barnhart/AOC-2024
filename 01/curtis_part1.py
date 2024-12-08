import sys

if __name__ == "__main__":
    llist, rlist = [], []
    for line in open(sys.argv[1], "r"):
        numbers = line.split("   ")
        llist.append(int(numbers[0]))
        rlist.append(int(numbers[1]))

    llist.sort()
    rlist.sort()

    solution = sum((abs(l - r) for l, r in zip(llist, rlist)))
    print("Solution: {:d}!".format(solution))

