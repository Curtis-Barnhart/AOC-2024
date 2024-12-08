import sys


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


if __name__ == "__main__":
    with open(sys.argv[1], "r") as file:
        lines = [
            [int(n) for n in line.split(" ")]
            for line in file.readlines()
        ]

    print("Solution: {:d}!".format(sum((is_safe(line) for line in lines))))

