#!/bin/bash

file=test.txt
file=real.txt

join -2 2 \
        <(awk '{print $1}' $file | sort) \
        <(awk '{print $2}' $file | sort | uniq -c | sed 's/^ *//') \
    | awk '{t+=$1*$2}END{print t}'

