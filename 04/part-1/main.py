from numpy import ndarray, array


class Grid:
    def __init__(self, v: str) -> None:
        self.values = [list(line) for line in v.split("\n")[:-1]]
        self.X = len(self.values[0])
        self.Y = len(self.values)
        print(f"{self.X=}")
        print(f"{self.Y=}")

    def at(self, coord: ndarray) -> str:
        if coord[0] < 0 or coord[1] < 0:
            raise IndexError()
        return self.values[coord[1]][coord[0]]

    def xmas_center(self, coord: ndarray) -> int:
        x, y = coord
        try:
            if self.at(array((x, y))) != "A":
                return 0
            if self.at(array((x - 1, y + 1))) == "M" and \
               self.at(array((x - 1, y - 1))) == "M" and \
               self.at(array((x + 1, y + 1))) == "S" and \
               self.at(array((x + 1, y - 1))) == "S":
                   return 1
            if self.at(array((x - 1, y + 1))) == "S" and \
               self.at(array((x - 1, y - 1))) == "S" and \
               self.at(array((x + 1, y + 1))) == "M" and \
               self.at(array((x + 1, y - 1))) == "M":
                   return 1
            if self.at(array((x - 1, y + 1))) == "M" and \
               self.at(array((x - 1, y - 1))) == "S" and \
               self.at(array((x + 1, y + 1))) == "M" and \
               self.at(array((x + 1, y - 1))) == "S":
                   return 1
            if self.at(array((x - 1, y + 1))) == "S" and \
               self.at(array((x - 1, y - 1))) == "M" and \
               self.at(array((x + 1, y + 1))) == "S" and \
               self.at(array((x + 1, y - 1))) == "M":
                   return 1
        except IndexError:
            pass
        return 0

    def xmas_origin(self, coord: ndarray) -> int:
        origin = coord.copy()
        total = 0
        if self.at(origin) != "X":
            return total
        for delta in (
            array((1, 0)),
            array((1, 1)),
            array((0, 1)),
            array((-1, 1)),
            array((-1, 0)),
            array((-1, -1)),
            array((0, -1)),
            array((1, -1)),
        ):
            origin = coord.copy()
            possible = True
            try:
                for letter in "MAS":
                    origin += delta
                    if self.at(origin) != letter:
                        possible = False
                        break
                if not possible:
                    continue
            except IndexError:
                continue
            total += 1

        return total
    
    def all_xmas(self) -> int:
        return sum((self.xmas_origin(array((x, y))) for x in range(self.X) for y in range(self.Y)))

    def all_xmas2(self) -> int:
        for y in range(self.Y):
            for x in range(self.X):
                center = self.xmas_center(array((x, y)))
                if center:
                    print(x, y, center)
        return sum((self.xmas_center(array((x, y))) for x in range(self.X) for y in range(self.Y)))


if __name__ == "__main__":
    g = Grid(open("../input.txt", "r").read())
    print("Solution: {:d}!".format(g.all_xmas()))
    print("Solution: {:d}!".format(g.all_xmas2()))

