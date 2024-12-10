#!python3

from itertools import starmap

file = "test.txt"
file = "real.txt"

def check(nums):
    diffs = starmap(int.__sub__,
        zip(nums[1:], nums)
            if nums[0] < nums[1] else
        zip(nums, nums[1:]))

    return all(map(lambda d: 1 <= d <= 3, diffs))

def check_small(nums, i):
    small = list(nums)
    del small[i]
    return check(small)
    
def check_line(line):
    nums = list(map(int, line.rstrip().split(" ")))
    return check(nums) or any(map(lambda i:check_small(nums, i), range(len(nums))))

with open(file) as fh:
    total = sum(1 for _ in filter(check_line, fh))

print("total %d"%total)
