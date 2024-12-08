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

