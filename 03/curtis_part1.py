import re
import sys

if __name__ == "__main__":
    with open(sys.argv[1], "r") as file:
        nums = re.findall(r"(?<=mul\()\d{1,3},\d{1,3}(?=\))", file.read())
        print("Solution: {:d}!".format(
            sum(int(a)*int(b) for a,b in (pair.split(",") for pair in nums))
        ))

