#!python3

import devin_graph as graph
import sys

file = 'test.txt'
file = 'real.txt'

lines = [line.rstrip() for line in open(file)]

up = {}
down = {}

def addin(m,k,v):
    if k in m:
        m[k].add(v)
    else:
        m[k]=set([v])

reports = []

first = True
for line in lines:
    if not line:
        first = False
        continue
    if first:
        splt=line.split("|")
        s0 = splt[0]
        s1 = splt[1]

        addin(up, s0, s1)
        addin(down, s1, s0)
    else:
        reports.append(line.split(","))

def graphOrder(report):
    report = set(report)

    g = graph.Graph()
    pairs = set()

    for pageNum1 in report:
        for pageNum2 in up[pageNum1].intersection(report):
            pairs.add((pageNum1, pageNum2))
        for pageNum2 in down[pageNum1].intersection(report):
            pairs.add((pageNum2, pageNum1))

    for pageNum1, pageNum2 in pairs:
        node1 = g.newNode(pageNum1)
        node2 = g.newNode(pageNum2)
        g.newEdge(node1,node2)

    status, order = graph.topoSort(g)
    if status == "CYCLE":
        print("CYCLE %s"%(repr(order)))
        sys.exit(1)
    return [n.id for n in order]


total = 0
for report in reports:
    sortedReport = graphOrder(report)
    if report == sortedReport:
        total += int(sortedReport[len(sortedReport)//2])

print("%d"%(total))
