#!/bin/bash

file=test.txt
file=real.txt

# original:
# ------------------------------------------------------------
# grep -o "mul([0-9][0-9]*,[0-9][0-9]*)" $file | sed 's/mul(//;s/,/ /;s/)//;' | awk '{t+=$1*$2}END{print t}'

# better:
grep -o "mul([0-9][0-9]*,[0-9][0-9]*)" $file | awk -F '[(,)]' '{t+=$2*$3}END{print t}'

