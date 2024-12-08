import sys


def remove_at(list_: list[int], index: int) -> list[int]:
    c = list_.copy()
    c.pop(index)
    return c


def is_safe(numbers) -> bool:
    up_or_down = None

    for a, b in zip(numbers, numbers[1:]):
        if up_or_down is None:
            up_or_down = b - a
            if abs(up_or_down) > 3 or up_or_down == 0:
                return False
        else:
            if up_or_down < 0 and b >= a \
            or up_or_down > 0 and b <= a \
            or a - b == 0 \
            or abs(a - b) > 3:
                return False
    return True


def is_safe_any(numbers) -> bool:
    if is_safe(numbers):
        return True
    for i in range(len(numbers)):
        if is_safe(remove_at(numbers, i)):
            return True
    return False


if __name__ == "__main__":
    with open(sys.argv[1], "r") as file:
        lines = [
            [int(x) for x in line.split(" ")]
            for line in file.readlines()
        ]

    print("Solution: {:d}!".format(sum((is_safe_any(line) for line in lines))))

