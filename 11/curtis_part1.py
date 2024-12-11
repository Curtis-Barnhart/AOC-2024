import sys
from functools import cache


class Stone:
    def __init__(
        self, 
        value: int, 
        left: "Stone | None" = None, 
        right: "Stone | None" = None
    ) -> None:
        self.v = value
        self.prev = left
        self.next = right

    def update(self) -> "Stone | None":
        vstr = str(self.v)
        if self.v == 0:
            self.v = 1
            return self.next
        if len(vstr) % 2 == 0:
            # If there are an odd num of digs
            new_left = Stone(int(vstr[:len(vstr)//2]))
            new_right = Stone(int(vstr[len(vstr)//2:]))
            connect(self.prev, new_left)
            connect(new_left, new_right)
            if self.next is None:
                new_right.next = None
            else:
                connect(new_right, self.next)
                # self.next.prev = new_right
                # new_right.next = self.next
            # connect(self, new_right)
            return new_right.next
        else:
            self.v *= 2024
            return self.next


def count(s: Stone | None) -> int:
    x: int = 0
    while (s is not None):
        x += 1
        s = s.next
    return x


def connect(s1: Stone, s2: Stone) -> None:
    s1.next = s2
    s2.prev = s1


def print_stones(s: Stone | None) -> None:
    if s is not None:
        print(s.v, end=" ")
        print_stones(s.next)


def stone_chain_contain(s: Stone | None, v: int) -> bool:
    while (s is not None):
        if s.v == v:
            return True
        s = s.next
    return False


stone_loops: dict[int, list[int]] = dict()


@cache
def after_B_becomes_N(seed: int, depth: int) -> int:
    s = Stone(seed)
    head = Stone(0)
    connect(head, s)
    s.update()

    if depth == 1:
        return count(head.next)
    else:
        it = head.next
        acc: int = 0
        while it is not None:
            acc += after_B_becomes_N(it.v, depth - 1)
            it = it.next
        return acc


if __name__ == "__main__":
    stones = open(sys.argv[1], "r").read().split(" ")
    stones = [int(n) for n in stones]

    acc = 0
    for n in stones:
        acc += after_B_becomes_N(n, 25)

    print(acc)

