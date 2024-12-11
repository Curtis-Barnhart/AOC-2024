#!python3

import sys

file = 'test.txt'
file = 'real.txt'

class StackedDeltaList(object):
    def __init__(self, mapping_or_list, initial=True):
        if initial:
            self.seedList = mapping_or_list
            self.mapping = dict((i, [i]) for i in self.seedList)
            self.last = self
        else:
            self.mapping = mapping_or_list
            self.next = None

    def blink(self):
        lastMapping = {}
        for key, values in self.last.mapping.items():
            for i in values:
                if i == 0:
                    lastMapping[i] = (1,)
                else:
                    s = "%d"%i
                    l = len(s)
                    if l%2 == 0:
                        h = l//2
                        lastMapping[i] = (int(s[:h]), int(s[h:]))
                    else:
                        lastMapping[i] = (i*2024,)
        lastObject = StackedDeltaList(lastMapping, False)
        self.last.next = lastObject
        self.last = lastObject

    def toList(self, key=None):
        if key == None:
            theList = self.seedList
        else:
            theList = self.mapping[key]

        if self.next:
            l = []
            for i in theList:
                l.extend(self.next.toList(i))
            return l;
        return theList

    def _clean(self):
        self.lens = {}
        if self.next:
            self.next._clean()

    def getLen(self, key=None):
        if key == None:
            self._clean()
            theList = self.seedList
        else:
            if key in self.lens:
                return self.lens[key]
            theList = self.mapping[key]

        if self.next:
            ln = sum(self.next.getLen(i) for i in theList)
        else:
            ln = len(theList)

        if key:
            self.lens[key] = ln
        return ln
            


with open(file) as fh:
    w = StackedDeltaList([int(i) for i in fh.read().rstrip().split(" ")])

for i in range(75):
    w.blink()
    #print("ln %d for %s"%(w.getLen(), w.toList()))

print("%d"%(w.getLen()))

