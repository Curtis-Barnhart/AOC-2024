import sys

from curtis_part1 import after_B_becomes_N


if __name__ == "__main__":
    stones = open(sys.argv[1], "r").read().split(" ")
    stones = [int(n) for n in stones]

    acc = 0
    for n in stones:
        acc += after_B_becomes_N(n, 75)

    print(acc)

