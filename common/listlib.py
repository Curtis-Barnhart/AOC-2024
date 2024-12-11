#!python3

class _StackedTransformList(object):
    def __init__(self, transformation):
        self.transformation = transformation
        self.next = None

    def _clean(self):
        self._cache = {}
        if self.next:
            self.next._clean()

    def compute(self, key, leafFunc, accumFunc):
        if key in self._cache:
            return self._cache[key]

        theList = self.transformation[key]

        if self.next:
            answer = accumFunc(self.next.compute(i, leafFunc, accumFunc) for i in theList)
        else:
            answer = leafFunc(theList)

        self._cache[key] = answer
        return answer

class StackedTransformList(object):
    def __init__(self, mapping_or_list):
        self.seedList = mapping_or_list
        self.transformation = dict((i, [i]) for i in self.seedList)
        self.last = self

    def addTransform(self, transform):
        lastTransformation = {}
        for values in self.last.transformation.values():
            for i in values:
                if i not in lastTransformation:
                    lastTransformation[i] = transform(i)
        newLastObject = _StackedTransformList(lastTransformation)
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
        return self.compute(lambda lst:len(lst), lambda iter1:sum(iter1))

    def toList(self):
        return self.compute(lambda lst:lst, lambda iter1:[item for iter2 in iter1 for item in iter2])

if __name__ == "__main__":
    def transform(i):
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

    stList = StackedTransformList([125, 17])

    for i in range(10):
        stList.addTransform(transform)
        print("step %d length %d for %s"%(i, stList.getLen(), " ".join(str(i) for i in stList.toList())))

    for i in range(10, 200):
        stList.addTransform(transform)
        print("step %d length %d"%(i, stList.getLen()))

