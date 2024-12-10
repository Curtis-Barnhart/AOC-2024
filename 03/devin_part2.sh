#!/bin/bash

file=test.txt
file=real.txt

# original:
# ------------------------------------------------------------
# egrep -o "do\(\)|don't\(\)|mul\([0-9][0-9]*,[0-9][0-9]*\)" $file | python3 -c '
# import sys
# go=True
# for line in sys.stdin:
#     if line.startswith("do("):
#         go=True
#     elif line.startswith("don"):
#         go=False
#     elif go:
#         print(line.rstrip())
# ' | sed 's/mul(//;s/,/ /;s/)//;' | awk '{t+=$1*$2}END{print t}'


# better:
egrep -o "do\(\)|don't\(\)|mul\([0-9][0-9]*,[0-9][0-9]*\)" $file | awk -F '[(,)]' '
BEGIN{go=1}
/^do\(/{go=1}
/^don/{go=0}
{t+=go*$2*$3}
END{print t}'
