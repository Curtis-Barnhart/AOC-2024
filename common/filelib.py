#!python3

import sys
import re

# code: lines, rows, cols = readLines(file, warnOnVarLen=False)
def readLines(file, warnOnVarLen=True):
    """
    read lines
    expect them to all be the same length

    returns a list of str
    """
    with open(file) as fh:
        lines = [line.rstrip() for line in fh]
    rows = len(lines)
    cols = max(len(line) for line in lines)
    if warnOnVarLen and cols != min(len(line) for line in lines):
        print("WARN: not all lines are the same length")
    return lines, rows, cols

def readGroupsOfLines(file):
    """
    read lines
    group them using a blank line as the group delimiter

    returns a list of list of str
    """
    groups = []
    group = []
    with open(file) as fh:
        for line in fh:
            line = line.rstrip()
            if line:
                group.append(line)
            else:
                if group:
                    groups.append(group)
                    group = []
    if group:
        groups.append(group)
    return groups

def readCharArrays(file):
    """
    read lines
    create a list of chars for each line

    returns a list of list of chars
    """
    lines, rows, cols = readLines(file)
    return [list(line) for line in lines]

def readInts(file):
    "returns a list of int"
    with open(file) as fh:
        return [int(line.rstrip()) for line in fh]

def readIntArrays(file):
    """
    returns a list of list of int
    all non-numeric and non-space chars are removed before processing
    """
    pat = re.compile("[^ [0-9]")
    with open(file) as fh:
        return [[int(n) for n in pat.subn("", line.strip())[0].split(" ")] for line in fh]

def readProps(file, regex="([^=]*)=(.*)", delim=" "):
    """
    each line has a space delimited list of name=value pairs
    each line is parsed into a dict of these name=value pairs
    empty lines become empty dict
    regex can be changed to identify other ways of parsing the name=value pairs

    returns a list of dict
    """
    pat = re.compile("^%s$"%regex)
    with open(file) as fh:
        lines = [line.rstrip().split(delim) for line in fh]
    answer = []
    for line in lines:
        matches = [pat.match(expr) for expr in line if expr]
        if not all(matches):
            print("ERROR: not all lines match")
            print("fails on [%s]"%", ".join(line for line, m in zip(filter(lambda a:a, line), matches) if not m))
            sys.exit(1)
        answer.append(dict((m.group(1), m.group(2)) for m in matches))
    return answer

def cast(t,s):
    if t == "s":
        return s
    if t == "i":
        return int(s)

def readRegex(file, regex, types=None):
    """
    use regex to parse each line (no need to add ^ or $ to the regex)
    the groups become the values of an list for each line
    types is a string with chars of "i" or "s", one for each group

    returns a list of list of (str or int)
    """
    with open(file) as fh:
        lines = [line.rstrip() for line in fh]
    pat = re.compile("^%s$"%regex)
    matches = [pat.match(line) for line in lines]
    if not all(matches):
        print("ERROR: not all lines match")
        print("fails on [%s]"%", ".join(line for line, m in zip(lines, matches) if not m))
        sys.exit(1)
    lines = [m.groups() for m in matches]
    if types:
        lines = [[cast(*pair) for pair in zip(types, line)] for line in lines]
    return lines

