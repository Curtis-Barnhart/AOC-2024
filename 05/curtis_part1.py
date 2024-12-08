import sys
from collections.abc import Callable, Iterable
from typing import Any


from curtis_util import Rule, Update


def sort_iter(src: Iterable[Any], sorter: Callable[[Any], int]):
    groups: dict[int, list[Any]] = dict()
    for item in src:
        if (category:=sorter(item)) in groups.keys():
            groups[category].append(item)
        else:
            groups[category] = [item]

    cat_count: int = max(groups.keys()) + 1
    all_lists: list[list[Any]] = [[]] * cat_count
    for i in range(cat_count):
        all_lists[i] = groups.get(i, [])

    return all_lists


if __name__ == "__main__":
    rules: list[Rule] = []
    updates: list[Update] = []

    section = 0
    with open(sys.argv[1], "r") as file:
        for line in file:
            line = line[:-1]
            if section == 0:
                if line == "":
                    section = 1
                else:
                    pages_str = line.split("|")
                    rules.append(Rule(int(pages_str[0]), int(pages_str[1])))
            else:
                pages_str = line.split(",")
                updates.append(Update([int(v) for v in pages_str]))

    up_invalid, up_valid = sort_iter(
        updates, 
        lambda u: int(all((u.satisfies(r) for r in rules)))
    )

    print("Solution: {:d}!".format(sum((
        update.middle for update in up_valid
    ))))

