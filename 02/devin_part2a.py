#!python3

file = "test.txt"
file = "real.txt"

def check(nums):
    diffs = (
        pair[0] - pair[1]
        for pair in (
            zip(nums[1:], nums)
                if nums[0] < nums[1] else
            zip(nums, nums[1:])))

    return all(1 <= d <= 3 for d in diffs)

def check_small(nums, i):
    small = list(nums)
    del small[i]
    return check(small)
    
def check_line(line):
    nums = list(int(n) for n in line.rstrip().split(" "))
    return check(nums) or any(check_small(nums, i) for i in range(len(nums)))

with open(file) as fh:
    total = sum(1 for line in fh if check_line(line))

print("total %d"%total)
