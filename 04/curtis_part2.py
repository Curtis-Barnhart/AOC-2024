import sys

from curtis_util import Grid


if __name__ == "__main__":
    g = Grid(open(sys.argv[1], "r").read())
    print("Solution: {:d}!".format(g.all_xmas2()))

