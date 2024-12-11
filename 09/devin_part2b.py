#!python3

# improvments:
#   make vars for sub-lists
#       more readable
#       more performance
#

import itertools as it

file = 'test.txt'
file = 'real.txt'


with open(file) as fh:
    disk = fh.read().rstrip()

# file digits: disk, free, disk, free, ...
# format as list<list<(type, id, size)>>
# this is a list of sub-lists, allowing cheap regional edits to the list while maintaining a form of random access
diskSpace = [[("d" if fId%2 == 0 else "f", fId//2, int(fLen))] for fId, fLen in zip(it.count(),disk)]

dIdxStart = len(diskSpace)-1

while True:
    # find next disk to move
    dIdx = dIdxStart
    while dIdx >= 0 and (not diskSpace[dIdx] or diskSpace[dIdx][-1][0] != "d"):
        dIdx -= 1
    if dIdx == -1:
        break
    dIdxStart = dIdx
    # simplify
    dSubList = diskSpace[dIdx]


    # find first free block where disk block fits
    fIdx = 0
    disk_sz = disk_sect = dSubList[-1][2]
    while fIdx < dIdx and diskSpace[fIdx] and (diskSpace[fIdx][-1][0] == "d" or diskSpace[fIdx][-1][2] < disk_sz):
        fIdx += 1
    # exit on free block search fail
    if dIdx == fIdx:
        dIdxStart -= 1
        continue
    # simplify
    fSubList = diskSpace[fIdx]


    # remove disk, replace with free
    disk_type, disk_id, disk_sz = disk_sect = dSubList.pop(-1)
    dSubList.append(('f', disk_id, disk_sz))


    # remove free block
    free_type, free_id, free_sz = free_sect = fSubList.pop(-1)

    # replace it with disk and free blocks
    if free_sz > disk_sz:
        fSubList.append(disk_sect)
        fSubList.append(("f", free_id, free_sz - disk_sz))
    elif free_sz < disk_sz:
        fSubList.append(("d", disk_id, free_sz))
        dSubList.append(("d", disk_id, disk_sz - free_sz))
    else:
        fSubList.append(disk_sect)


    # combind contiguous free blocks
    contig_free_sz = 0
    if len(dSubList) == 1 and diskSpace[dIdx-1] and diskSpace[dIdx-1][-1][0] == 'f':
        contig_free_sz += diskSpace[dIdx-1].pop(-1)[2]
    if dIdx+1 < len(diskSpace) and diskSpace[dIdx+1] and diskSpace[dIdx+1][0][0] == 'f':
        contig_free_sz += diskSpace[dIdx+1].pop(0)[2]
    if contig_free_sz:
        contig_free_sz += dSubList.pop(-1)[2]
        dSubList.append(('f', free_id, contig_free_sz))


answer1 = [(x_type, x_id, x_sz) for sec_list in diskSpace for x_type, x_id, x_sz in sec_list]
print("\n".join(map(str, answer1)))

cksum = 0
idx = 0
for x_type, x_id, x_sz in answer1:
    for i in range(x_sz):
        if x_type == 'd':
            cksum += x_id*idx
        idx += 1

print("cksum %d"%cksum)
