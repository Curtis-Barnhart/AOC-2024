import re
import sys

if __name__ == "__main__":
    with open(sys.argv[1], "r") as file:
        text = file.read()
    text = "do()" + text.replace("\n", "")
    text = re.sub(r"(do\(\)|don't\(\))", "\n\\1", text)
    text = "".join((line for line in text.split("\n") if line.startswith("do()")))

    nums = re.findall(r"(?<=mul\()\d{1,3},\d{1,3}(?=\))", text)
    print("Solution: {:d}!".format(
        sum(int(a)*int(b) for a,b in (pair.split(",") for pair in nums))
    ))

