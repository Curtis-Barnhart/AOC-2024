#!python3

import sys

file = 'test.txt'
file = 'real.txt'

class WackList(object):
    def __init__(self, back, mapping=None, initial=True):
        self.lens = {}
        if initial:
            with open(back) as fh:
                self.realList = [int(i) for i in fh.read().rstrip().split(" ")]
            self.mapping = dict((i, [i]) for i in self.realList)
        else:
            self.back = back
            self.mapping = mapping
            self.next = None
    def blink(self):
        mapping2 = {}
        for key, values in self.mapping.items():
            for i in values:
                if i == 0:
                    mapping2[i] = (1,)
                else:
                    s = "%d"%i
                    l = len(s)
                    if l%2 == 0:
                        h = l//2
                        mapping2[i] = (int(s[:h]), int(s[h:]))
                    else:
                        mapping2[i] = (i*2024,)
        self.next = WackList(self, mapping2, False)
        return self.next

    def toList(self, key=None):
        if key == None:
            theList = self.realList
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
            theList = self.realList
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
            


w = WackList(file)
we = w

for i in range(75):
    we = we.blink()
    # print("ln %d for %s"%(w.getLen(), w.toList()))

print("%d"%(w.getLen()))

