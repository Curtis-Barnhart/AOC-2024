#!python3

import itertools as it

file = 'test.txt'
file = 'real.txt'


# file digits: file, free, ...

disk = [line for line in open(file)][0].rstrip()


files = list(zip(it.count(), (int(d) for d in disk[0::2])))
frees = list(zip(it.count(), (int(d) for d in disk[1::2])))


diskSpace = [[("d" if fid%2 == 0 else "f", fid//2, int(flen))] for fid, flen in zip(it.count(),disk)]

#print("\n".join((repr(x) for x in diskSpace)))

backSearchStart = len(diskSpace)-1

while True:
    # find last disk to move
    i = backSearchStart
    while i >= 0 and (not diskSpace[i] or diskSpace[i][-1][0] != "d"):
        i -= 1
    if i == -1:
        break

    disk_type, disk_id, disk_sz = disk_sect = diskSpace[i][-1]
    backSearchStart = i
    #print("found disk %s"%repr(disk_sect))

    # find first free space where it fits
    j = 0
    while j < i and diskSpace[j] and (diskSpace[j][-1][0] == "d" or diskSpace[j][-1][2] < disk_sz):
        j += 1


    # exit if no space
    if i == j:
        backSearchStart -= 1
        continue

    # remove the disk space
    del diskSpace[i][-1]
    diskSpace[i].append(('f', disk_id, disk_sz))
    #print("ZAP %d"%i)

    # remove the free space
    free_type, free_id, free_sz = free_sect = diskSpace[j][-1]
    del diskSpace[j][-1]
    #print("found free %s"%repr(free_sect))

    if free_sz > disk_sz:
        diskSpace[j].append(disk_sect)
        diskSpace[j].append(("f", free_id, free_sz - disk_sz))
    elif free_sz < disk_sz:
        diskSpace[j].append(("d", disk_id, free_sz))
        diskSpace[i].append(("d", disk_id, disk_sz - free_sz))
    else:
        diskSpace[j].append(disk_sect)

    # connect contiguous free
    free_sz = 0
    if len(diskSpace[i]) == 1 and diskSpace[i-1] and diskSpace[i-1][-1][0] == 'f':
        free_sz += diskSpace[i-1][-1][2]
        del diskSpace[i-1][-1]
    if i+1 < len(diskSpace) and diskSpace[i+1] and diskSpace[i+1][0][0] == 'f':
        free_sz += diskSpace[i+1][0][2]
        del diskSpace[i+1][0]
    if free_sz:
        free_sz += diskSpace[i][-1][2]
        del diskSpace[i][-1]
        diskSpace[i].append(('f', free_id, free_sz))

    #print("-----")
    #print("\n".join(repr(x) for x in diskSpace))


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
