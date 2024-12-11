#!python3

import devin_maplib as ml

m = ml.CharMap("real.txt", "^")

def handleObject(m):
    "handle # chars, obsticles in the map"
    if m.beenHereBefore():
        return True
    m.moveBackward()
    m.turnRight()

steps = 1 # one for the place the guard is currently standing
def handleDot(m):
    "handle . chars, walk straight through and count the steps"
    global steps
    steps += 1
    m.setCharOnWalk("X")

m.regHandler("#", handleObject)
m.regHandler(".", handleDot)
m.walk()

m.unregHandler(".")

cycleCount = 0
def checkForCycle(c, row, col):
    "check if a point, when changed to a barrier, will cause a cycle in the guard's walk"
    global cycleCount
    m.lines[row][col] = "#"
    if m.walk():
        cycleCount += 1
    m.lines[row][col] = "X"

m.forAllDo("X", checkForCycle)

print("%d steps and %d possible cycle"%(steps, cycleCount))
