#!/bin/bash

file=test.txt
file=real.txt

paste \
        <(awk '{print $1}' $file | sort -n) \
        <(awk '{print $2}' $file | sort -n) \
    | awk 'func abs(x) { return (x<0) ? x * -1 : x }{t += abs($1-$2)} END{print t}'

