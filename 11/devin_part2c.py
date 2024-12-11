#!python3

import sys

file = 'real.txt'
file = 'test.txt'

class _StackedDeltaList(object):
    def __init__(self, mapping):
        self.mapping = mapping
        self.next = None

    def _clean(self):
        self._cache = {}
        if self.next:
            self.next._clean()

    def compute(self, key, leafFunc, accumFunc):
        if key in self._cache:
            return self._cache[key]

        theList = self.mapping[key]

        if self.next:
            answer = accumFunc(self.next.compute(i, leafFunc, accumFunc) for i in theList)
        else:
            answer = leafFunc(theList)

        self._cache[key] = answer
        return answer

class StackedDeltaList(object):
    def __init__(self, mapping_or_list):
        self.seedList = mapping_or_list
        self.mapping = dict((i, [i]) for i in self.seedList)
        self.last = self

    def applyToAll(self, f):
        lastMapping = {}
        for values in self.last.mapping.values():
            for i in values:
                if i not in lastMapping:
                    lastMapping[i] = f(i)
        newLastObject = _StackedDeltaList(lastMapping)
        self.last.next = newLastObject
        self.last = newLastObject

    def _clean(self):
        self._cache = {}
        if self.next:
            self.next._clean()

    def compute(self, leafFunc, accumFunc):
        self._clean()

        if self.next:
            answer = accumFunc(self.next.compute(i, leafFunc, accumFunc) for i in self.seedList)
        else:
            answer = accumFunc(self.seedList)

        self._clean()
        return answer

    def getLen(self):
        return self.compute(lambda lst:len(lst), lambda iter:sum(iter))

    def toList(self):
        return self.compute(lambda lst:lst, lambda iter1:[item for iter2 in iter1 for item in iter2])

def f(i):
    if i == 0:
        return (1,)
    else:
        s = "%d"%i
        l = len(s)
        if l%2 == 0:
            h = l//2
            return (int(s[:h]), int(s[h:]))
        else:
            return (i*2024,)

with open(file) as fh:
    w = StackedDeltaList([int(i) for i in fh.read().rstrip().split(" ")])

for i in range(10):
    w.applyToAll(f)
    print("ln %d for %s"%(w.getLen(), " ".join(str(i) for i in w.toList())))

print("%d"%(w.getLen()))

