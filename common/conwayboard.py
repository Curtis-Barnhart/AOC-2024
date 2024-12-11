#!python3

# coordinates are as (row, col)
# row is a line number, bigger means down
# col is a column, bigger means right

import sys
import re

class ConwayBoard(object):

    def __init__(self, file):
        self.lines = [line.rstrip() for line in open(file)]
        self.rows, self.cols = (len(self.lines), len(self.lines[0]))

    #####################
    # generate
    #####################

    def generateBoard(self):
        lines = ["".join(self.generateCell(row, col) for col in range(self.cols)) for row in range(self.rows)]
        change = lines != self.lines
        self.lines = lines
        return change

    def generateCell(self, row, col):
        return " "

    #####################
    # query the board
    #####################

    def getChar(self, row, col):
        return self.lines[row][col]

    def getChars(self, row, colStart, colEnd, defChar=' '):
        colEnd += 1
        if colStart < 0:
            return defChar*(-colStart) + self.lines[row][0:colEnd]
        elif colEnd > self.cols:
            return self.lines[row][colStart:] + defChar*(colEnd-self.cols)
        else:
            return self.lines[row][colStart:colEnd]

    def getBlock(self, row, col, size):
        return "".join(self.getChars(row+i, col-size, col+size) for i in range(-size, size+1))

    def overThreshold(self, row, col, size, char, minCount):
        row1 = max(row - size, 0)
        row2 = min(row + size + 1, self.rows)
        col1 = max(col - size, 0)
        col2 = min(col + size + 1, self.cols)
        count = 0
        for i in range(row1, row2):
            r = self.lines[i]
            for j in range(col1, col2):
                if (i != row or j != col) and r[j] == char:
                    count += 1
                    if count == minCount:
                        return True

    #####################
    # examine global properties
    #####################

    def countChars(self, char):
        count = 0
        for row in range(self.rows):
            r = self.lines[row]
            for col in range(self.cols):
                if r[col] == char:
                    count += 1
        return count

    def __str__(self):
        return "\n".join(self.lines)

