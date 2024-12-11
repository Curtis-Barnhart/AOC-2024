#!python3

# qsort(list, comparator)
# mergesort(iterable1, iterable2, comparator)

def _qsort(lst, comp, top, bottom):
    l = bottom - top + 1

    if l < 2:
        return

    top2 = top
    bottom2 = bottom

    center = (bottom + top) // 2
    pivot = lst[center]

    while top2 <= bottom2:
        while top2 <= bottom2 and comp(lst[top2], pivot) <= 0:
            top2 += 1
        while top2 <= bottom2 and comp(pivot, lst[bottom2]) < 0:
            bottom2 -= 1
        if top2 <= bottom2:
            tmp = lst[top2]
            lst[top2] = lst[bottom2]
            lst[bottom2] = tmp

    if top2-1 == bottom:
        tmp = lst[center]
        lst[center] = lst[bottom]
        lst[bottom] = tmp
        _qsort(lst, comp, top, bottom-1)
    elif bottom2+1 == top:
        tmp = lst[center]
        lst[center] = lst[top]
        lst[top] = tmp
        _qsort(lst, comp, top+1, bottom)
    else:
        _qsort(lst, comp, top, bottom2)
        _qsort(lst, comp, top2, bottom)

def qsort(lst, comp):
    _qsort(lst, comp, 0, len(lst)-1)

EOM=(None, "END")
def mergesort(iterable1, iterable2, comp):
    iter1 = iter(iterable1)
    iter2 = iter(iterable2)
    v1 = next(iter1, EOM)
    v2 = next(iter2, EOM)
    while v1 != EOM or v2 != EOM:
        if v1 == EOM or (v2 != EOM and comp(v1, v2) > 0):
            yield v2
            v2 = next(iter2, EOM)
        else:
            yield v1
            v1 = next(iter1, EOM)

if __name__ == "__main__":
    import random
    for cnt in range(50):
        a = [random.randint(-1000, 1000) for i in range(random.randint(0,30))]
        qsort(a, lambda a,b:a-b)
        b = list(a)
        b.sort()
        print("%s sorted %s"%(a == b, a))

    print("mergsort %s"%[x for x in mergesort(range(0,20,2), range(1,20,2), lambda a,b:a-b)])

