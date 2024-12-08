from collections.abc import Callable, Iterable
from functools import cmp_to_key
from typing import Any


class Rule:
    def __init__(self, prev: int, next: int) -> None:
        self.prev: int = prev
        self.next: int = next


class Update:
    def __init__(self, pages: list[int]) -> None:
        self.middle: int = pages[len(pages)//2]
        self.page_list: list[int] = pages.copy()
        self.pages: dict[int, int] = {
            page: index
            for index, page in enumerate(pages)
        }

    def satisfies(self, rule: Rule) -> bool:
        if rule.next in self.pages.keys():
            return self.pages.get(rule.prev, -1) < self.pages[rule.next]
        return True
    

class Comparator:
    def __init__(self, rules: list[Rule]) -> None:
        self.orders: dict[int, set[int]] = dict()
        for rule in rules:
            if rule.prev in self.orders.keys():
                self.orders[rule.prev].add(rule.next)
            else:
                self.orders[rule.prev] = {rule.next}

    def cmp(self, n1, n2) -> int:
        if n1 in self.orders.keys():
            if n2 in self.orders[n1]:
                return -1
        if n2 in self.orders.keys():
            if n1 in self.orders[n2]:
                return 1
        return 0


def sort_pages(update: Update, comparator: Comparator) -> Update:
    page_list = update.page_list.copy()
    page_list.sort(key=cmp_to_key(lambda n1, n2: comparator.cmp(n1, n2)))
    return Update(page_list)


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
    with open("../input.txt", "r") as file:
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

    # test_up_invalid, test_up_valid = sort_iter(
    up_invalid, up_valid = sort_iter(
        updates, 
        lambda u: int(all((u.satisfies(r) for r in rules)))
    )

    print("Solution: {:d}!".format(sum((
        update.middle for update in up_valid
    ))))

    comparator = Comparator(rules)
    up_sorted: list[Update] = []
    for update in up_invalid:
        up_sorted.append(sort_pages(update, comparator))

    print("Solution: {:d}!".format(sum((
        update.middle for update in up_sorted
    ))))

