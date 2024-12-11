#!python3

# coordinates are as (row, col)
# row is a line number, bigger means down
# col is a column, bigger means right

import sys
import re

#
# class CharMap
#   -- short wandering paths
#       setNearDirs(self, dirs):
#       pathCount(self, path):
#       endCount(self, path):
#   -- walking navigation
#       validPoint(self, row, col)
#       setStart(self, line, col)
#       setDelta(self, dLines, dCols)
#       moveForward(self)
#       moveBackward(self)
#       turnRight(self)
#       turnLeft(self)
#       turnRight45(self)
#       turnLeft45(self)
#       turnBack(self)
#       beenHereBefore(self)
#   -- walking the map
#       regHandler(self, c, f)
#       unregHandler(self, c)
#       walk(self)
#       setCharOnWalk(self, c)
#   -- examine the map
#       getCharFast(self, row, col)
#       getChar(self, row, col, defChar=' ')
#       getPoints(self, regex)
#       allPointsIter(self)
#   -- manipulate the map
#       forAllDo(self, c, f)
#       setChar(self, c, row, col)
#       drawLine(row1, col1, row2, col2, points=None, char=None, goRight=False, goLeft=False, goCenter=True, fill=True, inclusive=True):

def _addToMultiMap(d, k, v):
    if k in d:
        d[k].add(v)
    else:
        d[k] = set([v])

class CharMap(object):

    def __init__(self, file, startWalkChar=None, startDelta=(-1,0), wrapHoriz=False, wrapVert=False):
        self.wrapHoriz = wrapHoriz
        self.wrapVert = wrapVert
        if file == "40x40-test":
            self.lines = [["." for col in range(40)] for row in range(40)]
            self.rows, self.cols = (40, 40)
            self.row, self.col = (20, 20)
            self.start = (20,20)
        else:
            self.lines = [list(line.rstrip()) for line in open(file)]
            self.rows, self.cols = (len(self.lines), len(self.lines[0]))

            if startWalkChar:
                startRow = 0
                for line in self.lines:
                    if startWalkChar in line:
                        break
                    startRow += 1
                startCol = line.index(startWalkChar)
            else:
                startRow, startCol = 0, 0
            self.start = (startRow, startCol)
        if max(len(line) for line in self.lines) != min(len(line) for line in self.lines):
            print("ERROR: not all lines are the same length")
            sys.exit(1)
        self.startDelta = startDelta
        self.dRow, self.dCol = startDelta
        self.handlers = {}

    ####################
    # short wandering paths
    ####################

    def setNearDirs(self, dirs):
        "set the directions used by findNearIter"
        if dirs == 4:
            self.dirs = [(1,0),(0,1),(-1,0),(0,-1)]
        elif dirs == 8:
            self.dirs = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        else:
            print("ERROR: %d directions not supported for a map"%dirs)

    def nearPointsIter(self, row, col):
        for dr, dc in self.dirs:
            vp = self.validPoint(row+dr, col+dc)
            if vp:
                yield vp

    def findNearIter(self, row, col, char):
        "iterate over the coordinages (row, col) with a given chars near a point"
        for dr, dc in self.dirs:
            vp = self.validPoint(row+dr, col+dc)
            if vp and self.getCharFast(*vp) == char:
                yield vp

    def _pathCount(self, row, col, path, pIdx):
        if pIdx == len(path):
            return 1
        char = path[pIdx]
        return sum(self._pathCount(*fork, path, pIdx+1) for fork in self.findNearIter(row, col, char))

    def pathCount(self, path):
        "count how many paths can be found from path beginnings to path endings"
        char = path[0]
        return sum(self._pathCount(row, col, path, 1) for row, col, c in self.allPointsAndCharIter() if c == char)

    def _endCount(self, row, col, path):
        points = [(row, col)]
        for i in range(1,len(path)):
            newPoints = set()
            for point in points:
                newPoints.update(self.findNearIter(*point, path[i]))
            points = newPoints
        return len(points)

    def endCount(self, path):
        "count how many path ends can be found from path beginnings"
        total = 0
        char = path[0]
        for row, col in self.allPointsIter():
            if self.lines[row][col] == char:
                total += self._endCount(row, col, path)
        return total

    def forNearPointsDo(self, f):
        """
            call f(point1, char1, point2, char2) for all points that are near to each other
        """
        for row, col in self.allPointsIter():
            for point in self.nearPointsIter(row, col):
                f((row, col), self.getCharFast(row, col), point, self.getCharFast(*point))


    ####################
    # walking navigation
    ####################

    def validPoint(self, row, col):
        row2 = (row + 100*self.rows)%self.rows
        col2 = (col + 100*self.cols)%self.cols
        if not self.wrapVert and row2 != row:
            return None
        if not self.wrapHoriz and col2 != col:
            return None
        return (row2, col2)

    def setStart(self, line, col):
        self.start = (line, col)

    def setDelta(self, dLines, dCols):
        self.startDelta = (dLines, dCols)

    def moveForward(self):
        self.row += self.dRow
        self.col += self.dCol

    def moveBackward(self):
        self.row -= self.dRow
        self.col -= self.dCol

    def turnRight(self):
        # (0,1) -> (1,0) -> (0,-1) -> (-1,0) -> ...
        # (1,1) -> (1,-1) -> (-1,-1) -> (-1, 1) -> ...
        self.dRow, self.dCol = (self.dCol, -self.dRow)

    def turnLeft(self):
        # (0,1) -> (-1,0) -> (0,-1) -> (1,0) -> ...
        # (1,1) -> (-1,1) -> (-1,-1) -> (1,-1) -> ...
        self.dRow, self.dCol = (-self.dCol, self.dRow)

    def turnRight45(self):
        # (0,1) -> (1,0) -> (0,-1) -> (-1,0) -> ...
        #      (1,1) -> (1,-1) -> (-1,-1) -> (-1, 1) -> ...
        if self.dRow == 0:
            self.dRow = self.dCol
        elif self.dCol == 0:
            self.dCol = -self.dRow
        elif self.dRow == self.dCol:
            self.dCol = 0
        else:
            self.dRow = 0

    def turnLeft45(self):
        # (0,1) -> (-1,0) ->  (0,-1) -> (1,0) -> ...
        #     (-1,1) -> (-1,-1) -> (1,-1) -> (1,1) -> ...
        if self.dRow == 0:
            self.dRow = -self.dCol
        elif self.dCol == 0:
            self.dCol = self.dRow
        elif self.dRow == self.dCol:
            self.dRow = 0
        else:
            self.dCol = 0

    def turnBack(self):
        self.dRow, self.dCol = (-self.dCol, -self.dRow)

    def beenHereBefore(self):
        step = (self.row, self.col, self.dRow, self.dCol)
        if step in self.walked:
            return True
        self.walked.add(step)

    ####################
    # walking the map
    ####################

    def regHandler(self, c, f):
        """
            f(CharMap.self) is called when c is steped on
        """
        self.handlers[c] = f

    def unregHandler(self, c):
        del self.handlers[c]

    def walk(self):
        self.walked = set()
        self.row, self.col = self.start
        self.dRow, self.dCol = self.startDelta
        while True:
            self.moveForward()

            vp = self.validPoint(self.row, self.col)
            if not vp:
                return False
            self.row, self.col = vp

            c = self.lines[self.row][self.col]
            handler = self.handlers.get(c, None)
            if handler:
                answer = handler(self)
                if answer:
                    return answer

    def setCharOnWalk(self, c):
        self.lines[self.row][self.col] = c

    ####################
    # examine the map
    ####################

    def getCharFast(self, row, col):
        return self.lines[row][col]

    def getChar(self, row, col, defChar=' '):
        vp = self.validPoint(row, col)
        if vp:
            return self.lines[vp[0]][vp[1]]
        else:
            return defChar

    def getPoints(self, regex):
        """
        returns a map from char to a set of (row,col) points where that char is found
        """
        answer = {}

        def f(c, row, col):
            _addToMultiMap(answer, c, (row, col))
        self.forAllDo(regex, f)

        return answer
        
    def allPointsIter(self):
        for row in range(self.rows):
            for col in range(self.cols):
                yield (row, col)

    def allPointsAndCharIter(self):
        for row in range(self.rows):
            for col in range(self.cols):
                yield (row, col, self.lines[row][col])

    ####################
    # manipulate the map
    ####################

    def forAllDo(self, regex, f):
        pat = re.compile("[%s]"%regex)
        for row, col, c in self.allPointsAndCharIter():
            if pat.match(c):
                f(c, row, col)

    def setChar(self, c, row, col):
        self.lines[row][col] = c

    def _drawLine(self, row, col, dRow, dCol, stopRow, stopCol, points, char, inclusive):
        if not inclusive:
            row += dRow
            col += dCol
        vp = self.validPoint(row, col)
        while vp:
            row, col = vp

            if row == stopRow and col == stopCol:
                if inclusive:
                    points.add((row,col))
                    if char:
                        self.setChar(char, row, col)
                return

            points.add((row,col))
            if char:
                self.setChar(char, row, col)

            vp = self.validPoint(row + dRow, col + dCol)

    def drawLine(self, row1, col1, row2, col2, points=None, char=None, goRight=False, goLeft=False, goCenter=True, fill=True, inclusive=True):
        if points == None:
            points = set()

        dRow = row2-row1
        dCol = col2-col1

        if not dRow and not dCol:
            print("ERROR: line needs two distinct points")
            return

        if fill:
            for p in range(2, max(abs(dRow), abs(dCol))+1):
                while p*(dRow // p) == dRow and p*(dCol // p) == dCol:
                    dRow //= p
                    dCol //= p

        if goRight:
            self._drawLine(row2, col2, dRow, dCol, row1, col1, points, char, inclusive)

        if goLeft:
            self._drawLine(row1, col1, -dRow, -dCol, row2, col2, points, char, inclusive)

        if goCenter:
            self._drawLine(row1, col1, dRow, dCol, row2, col2, points, char, inclusive)

        return points

    ####################
    # misc
    ####################

    def __str__(self):
        return "\n".join("".join(line) for line in self.lines)

if __name__ == "__main__":
    m = CharMap("40x40-test")
    # m = CharMap("40x40-test", wrapHoriz=True, wrapVert=True)
    m.setCharOnWalk("O")
    if False:
        # m.turnBack()
        for i in range(7):
            for j in range(4):
                m.moveForward()
                m.setCharOnWalk("x")
            m.turnRight45()
    if False:
        #m.turnRight45()
        #m.turnLeft45()
        for i in range(3):
            for j in range(4):
                m.moveForward()
                m.setCharOnWalk("z")
            #m.turnRight()
            m.turnLeft()

    fill=True
    inclusive=True

    m.drawLine(38, 31+0, 39, 31+0, char="|", goRight=True, goLeft=True)
    m.drawLine(38, 31+3, 39, 31+3, char="|", goRight=True, goLeft=True)

    print("line I %s"%m.drawLine(  4, 31,  4+3,  31+3, fill=fill, inclusive=inclusive, char="I"))
    print("line O %s"%m.drawLine(  6, 31,  6+3,  31+3, fill=fill, inclusive=inclusive, char="O", goRight=True, goLeft=True, goCenter=False))
    print("line R %s"%m.drawLine(  8, 31,  8+3,  31+3, fill=fill, inclusive=inclusive, char="R", goRight=True))
    print("line L %s"%m.drawLine( 10, 31, 10+3,  31+3, fill=fill, inclusive=inclusive, char="L", goLeft=True))
    print("line A %s"%m.drawLine( 12, 31, 12+3,  31+3, fill=fill, inclusive=inclusive, char="A", goRight=True, goLeft=True))

    # vertical lines
    print("line I %s"%m.drawLine( 10, 10, 13,  10, fill=fill, inclusive=inclusive, char="I"))
    print("line O %s"%m.drawLine( 10, 11, 13,  11, fill=fill, inclusive=inclusive, char="O", goRight=True, goLeft=True, goCenter=False))
    print("line R %s"%m.drawLine( 10, 12, 13,  12, fill=fill, inclusive=inclusive, char="R", goRight=True))
    print("line L %s"%m.drawLine( 10, 13, 13,  13, fill=fill, inclusive=inclusive, char="L", goLeft=True))
    print("line A %s"%m.drawLine( 10, 14, 13,  14, fill=fill, inclusive=inclusive, char="A", goRight=True, goLeft=True))

    # horizontal lines
    print("line I %s"%m.drawLine( 30, 31, 30,  31+3, fill=fill, inclusive=inclusive, char="I"))
    print("line O %s"%m.drawLine( 31, 31, 31,  31+3, fill=fill, inclusive=inclusive, char="O", goRight=True, goLeft=True, goCenter=False))
    print("line R %s"%m.drawLine( 32, 31, 32,  31+3, fill=fill, inclusive=inclusive, char="R", goRight=True))
    print("line L %s"%m.drawLine( 33, 31, 33,  31+3, fill=fill, inclusive=inclusive, char="L", goLeft=True))
    print("line A %s"%m.drawLine( 34, 31, 34,  31+3, fill=fill, inclusive=inclusive, char="A", goRight=True, goLeft=True))

    m.drawLine(10, 0, 10+1, 2, char="a", goRight=True)
    m.drawLine(10, 0, 10+1, 3, char="b", goRight=True)
    m.drawLine(10, 0, 10+1, 4, char="c", goRight=True)
    m.drawLine(10, 0, 10+1, 5, char="d", goRight=True)
    m.drawLine(10, 0, 10+1, 6, char="e", goRight=True)

    print(str(m))

