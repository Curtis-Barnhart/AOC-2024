#!python3

from itertools import starmap

file = "test.txt"
file = "real.txt"

total = 0
for line in open(file):
    nums = list(map(int, line.rstrip().split(" ")))

    ds = starmap(int.__sub__, zip(nums, nums[1:]))

    if nums[0] < nums[1]:
        ds = map(int.__neg__, ds)

    if all(map(lambda d: 1 <= d <= 3, ds)):
        total += 1

print("total %d"%total)
