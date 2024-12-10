#!python3

import heapq

MAX_NODES = 1000000

# classes:
#   Node
#   Edge
#   Graph
#
# funcs:
#   shortestWgt
#   longestWgt
#   maxFlowPath
#   maxFlowGraph
#   topoSort
#

class Node(object):
    gid = -1;

    def _nextId():
        Node.gid += 1
        return Node.gid

    def __init__(self, id=None):
        self.id = id if id != None else Node._nextId()
        self.esOut = {}
        self.esIn = {}

    def _addStartEdge(self, e):
        if e.nEnd.id in self.esOut:
            print("ERROR: node %d already has an edge out of node %d"%(self.id, e.nEnd.id))
            return
        self.esOut[e.nEnd.id] = e

    def _addEndEdge(self, e):
        if e.nStart.id in self.esIn:
            print("ERROR: node %d already has an edge into node %d"%(self.id, e.nEnd.id))
            return
        self.esIn[e.nStart.id] = e

    def getBackPath(self, l=None):
        if l == None:
            l = []
        if self.back:
            self.back.getBackPath(l)
        l.append(self.id)
        return l

    def __lt__(self, other):
        return self.wgt < other.wgt

    def __str__(self):
        return self.nStr()

    def nStr(self, showWhat):
        s = ""
        if "back" in showWhat and self.back != None:
            s = " back %d"%self.back.id
        return "Node(%s) in(%s) out(%s)%s"%(
            self.id,
            # things coming in, show the nStarting node
            ",".join(str(e.nStart.id) for e in self.esIn.values()),
            # things going out, show the nEnd node
            ",".join(
                e.eStr(showWhat)
                for e in self.esOut.values()),
            s)

class Edge(object):
    gid = -1;

    def _nextId():
        Edge.gid += 1
        return Edge.gid

    def __init__(self, nStart, nEnd, id=None, wgt=1):
        self.id = id if id != None else Edge._nextId()
        self.nStart = nStart
        self.nEnd = nEnd
        self.wgt = wgt
        nStart._addStartEdge(self)
        nEnd._addEndEdge(self)

    def eStr(self, showWhat):
        ss = []
        ss.append("%d"%self.nEnd.id)
        if "flow" in showWhat:
            ss.append("flow %d of %d"%(self.flow, self.wgt))
        else:
            ss.append("wgt %d"%self.wgt)
        return " ".join(ss)

    def __str__(self):
        return "Edge(%s)"%self.id

class ExitEdge(object):
    def __init__(self, eParent, nParent):
        self.id = eParent.id
        self.wgt = eParent.wgt
        self.nStart = eParent.nStart
        self.nEnd = eParent.nEnd
        self.nParent = nParent
        self.isDel = False

    def __lt__(self, other):
        return self.wgt < other.wgt or self.id < other.id

    def __str__(self):
        return "ExitEdge(%s to %s wgt %d parent_is %s)"%(self.nStart.id, self.nEnd.id, self.wgt, self.nParent.id)

class Graph(object):
    ###############################
    # creation
    ###############################

    def __init__(self, directed=True):
        self.ns = {}
        self.es = {}
        self.directed = directed
        self.showWhat = set()
        self.esExit = None

    def newNode(self, id=None):
        if id in self.ns:
            return self.ns[id]
        node = Node(id)
        self.ns[node.id] = node
        return node

    def newEdge(self, nStart, nEnd, id=None, wgt=1):
        edge = Edge(nStart, nEnd, id, wgt)
        self.es[edge.id] = edge
        if not self.directed:
            if id:
                id = id + MAX_NODES
            edge = Edge(nEnd, nStart, id, wgt)
            self.es[edge.id] = edge
        return edge

    def remoteEdge(self, e):
        del e.nStart.esOut[e.nEnd.id]
        del e.nEnd.esIn[e.nStart.id]
        del self.es[e.id]

    ###############################
    # Sub graphs
    ###############################

    def newSubGraph(self):
        sg = Graph(directed = self.directed)
        sg.parent = self
        sg.esExit = []
        return sg

    def cpEdge(self, e):
        if e.id in self.es:
            print("ERROR: cp edge already copied")
            return

        nEdgeStart = self.ns[e.nStart.id]
        nEdgeEnd = self.ns[e.nEnd.id]

        eNew = self.newEdge(nEdgeStart, nEdgeEnd, id=e.id, wgt=e.wgt)
        eParent = self.parent.es[e.id]

    def cpNode(self, nParent):
        if nParent.id in self.ns:
            print("ERROR: cp node already copied")
            return

        nNew = self.newNode(nParent.id)

        for e in self.esExit:
            if (e.nStart.id in self.ns) ^ (e.nEnd.id in self.ns):
                e.isDel = True

        for e in nParent.esOut.values():
            if e.nEnd.id not in self.ns:
                if e not in self.esExit:
                    # include in esExit
                    eNew = ExitEdge(e, e.nEnd)
                    heapq.heappush(self.esExit, eNew)

        for e in nParent.esIn.values():
            if e.nStart.id not in self.ns:
                if e not in self.esExit:
                    # include in esExit
                    eNew = ExitEdge(e, e.nStart)
                    heapq.heappush(self.esExit, eNew)

    ###############################
    # stringify
    ###############################

    def setShow(self, value):
        self.showWhat = set(value)

    def __str__(self):
        l = []
        for n in self.ns.values():
            l.append("  " + n.nStr(self.showWhat))
        if self.esExit:
            l.append("  subgraph exits: " + ", ".join(str(e) for e in self.esExit if not e.isDel))
        return "\n".join(l)

    ###############################
    # internal
    ###############################

    def _unvisitNodes(self):
        for n in self.ns.values():
            n.visited1 = False
            n.visited2 = False
            n.back = None

    def _zeroEdgeFlow(self):
        for e in self.es.values():
            e.flow = 0


def maxFlowPath(g, nStart, nEnd):
    """
    returns (smallest edge weight along the path, list of nodes along the path)
    returns None if no path exists with all edges having wgt-flow greater than 0
    """
    g._unvisitNodes()
    nStart.wgt = -1e200
    nStart.visited1 = True
    heap = [nStart]
    while heap:
        # get smallest weighted node in the heap
        nEdgeStart = heapq.heappop(heap)
        if nEdgeStart.id == nEnd.id:
            return (-nEdgeStart.wgt, nEdgeStart.getBackPath())
        for e in nEdgeStart.esOut.values():
            nEdgeEnd = e.nEnd
            if nEdgeEnd.id != nStart.id:
                edgeFlow = min(e.wgt-e.flow, -nEdgeStart.wgt)
                if edgeFlow > 0:
                    maxWgt = max(nEdgeStart.wgt, -edgeFlow)
                    if not nEdgeEnd.visited1 or nEdgeEnd.wgt < maxWgt:
                        nEdgeEnd.back = nEdgeStart
                        nEdgeEnd.wgt = maxWgt
                        nEdgeEnd.visited1 = True
                        heapq.heappush(heap, nEdgeEnd)

def shortestWgt(g, nStart, nEnd):
    g._unvisitNodes()
    nStart.wgt = 0
    nStart.visited1 = True
    heap = [nStart]
    while heap:
        # get smallest weighted node in the heap
        nEdgeStart = heapq.heappop(heap)
        if nEdgeStart.id == nEnd.id:
            return (nEdgeStart.wgt, nEdgeStart.getBackPath())
        for e in nEdgeStart.esOut.values():
            nEdgeEnd = e.nEnd
            pathWgt = nEdgeStart.wgt + e.wgt
            if not nEdgeEnd.visited1 or nEdgeEnd.wgt > pathWgt:
                nEdgeEnd.back = nEdgeStart
                nEdgeEnd.wgt = pathWgt
                nEdgeEnd.visited1 = True
                heapq.heappush(heap, nEdgeEnd)

def _longHardWay(nStart, nEnd, wgt):
    nStart.visited1 = True
    oldLong = None
    for e in nStart.esOut.values():
        nxt = e.nEnd
        if nxt.id == nEnd.id:
            nxt.back = nStart
            newLong = (wgt + e.wgt, nxt.getBackPath())
        elif not nxt.visited1:
            nxt.back = nStart
            newLong = _longHardWay(nxt, nEnd, wgt + e.wgt)
        else:
            continue
        if newLong and (not oldLong or oldLong[0] < newLong[0]):
            oldLong = newLong
    nStart.visited1 = False
    return oldLong

def _topoSort(order, n):
    if not n.visited1:
        n.visited1 = True
        for e in n.esOut.values():
            cycle = _topoSort(order, e.nEnd)
            if cycle:
                if cycle == "CYCLE":
                    return [e.nEnd]
                else:
                    if len(cycle) <= 1 or cycle[0].id != cycle[-1].id:
                        cycle.append(e.nEnd)
                    return cycle
        order.append(n)
        n.visited2 = True
    elif not n.visited2:
        return "CYCLE"

def topoSort(g):
    """
    returns ("CYCLE", list of node) or ("ORDER, list of nodes)
    """
    g._unvisitNodes()
    order = []
    for n in g.ns.values():
        cycle = _topoSort(order, n)
        if cycle:
            cycle.reverse()
            return ("CYCLE", cycle)
    order.reverse()
    return ("ORDER", order)

def longestWgt(g, nStart, nEnd):
    status, ts = topoSort(g)
    if status == "ORDER":
        g._unvisitNodes()
        findStart = False
        for n in ts:
            if not findStart:
                if n.id == nStart.id:
                    n.wgt = 0
                    n.visited1 = True
                    n.back = None
                    findStart = True
            elif n.id == nEnd.id:
                return (n.wgt, n.getBackPath())
            if findStart:
                for e in n.esOut.values():
                    wgt = n.wgt + e.wgt
                    if not e.nEnd.visited1 or e.nEnd.wgt < wgt:
                        e.nEnd.wgt = wgt
                        e.nEnd.back = n
                        e.nEnd.visited1 = True
    else:
        g._unvisitNodes()
        nStart.wgt = 0
        nStart.back = None
        return _longHardWay(nStart, nEnd, 0)

def maxFlowGraph(g, nStart, nEnd):
    g._zeroEdgeFlow()
    totalFlow = 0
    path = maxFlowPath(g, nStart, nEnd)
    while (path):
        flow, nodePath = path
        totalFlow += flow
        for i in range(len(nodePath)-1):
            nEdgeStart = g.ns[nodePath[i]]
            eFwd = nEdgeStart.esOut[nodePath[i+1]]
            eFwd.flow += flow
            nEdgeEnd = eFwd.nEnd

            if nEdgeStart.id in nEdgeEnd.esOut:
                eBack = nEdgeEnd.esOut[nEdgeStart.id]
                overlap = min(eBack.flow, eFwd.flow)
                if overlap:
                    eBack.flow -= overlap
                    eFwd.flow -= overlap

        path = maxFlowPath(g, nStart, nEnd)
    return totalFlow

def connectedComponents(g):
    pass

def minSpanningTree(g):
    g2 = g.newSubGraph()
    n = next(n for n in g.ns.values())
    g2.cpNode(n)
    while g2.esExit:
        e = heapq.heappop(g2.esExit)
        if e.isDel:
            continue

        g2.cpNode(e.nParent)
        g2.cpEdge(e)
    return g2

if __name__ == "__main__":
    g = Graph(directed=True)
    n0 = g.newNode()
    n1 = g.newNode()
    n2 = g.newNode()
    n3 = g.newNode()

    g.newEdge(n0,n1,wgt=10)
    g.newEdge(n0,n2,wgt=30)
    g.newEdge(n1,n3,wgt=10)
    g.newEdge(n2,n3,wgt=10)

    e12 = g.newEdge(n1,n2,wgt=50)
    e21 = g.newEdge(n2,n1,wgt=60)

    short_path = shortestWgt(g, n0, n3)
    print("short: %s"%repr(short_path))

    long_path = longestWgt(g, n0, n3)
    print("long: %s"%repr(long_path))

    flow = maxFlowGraph(g, n0, n3)
    g.setShow(["flow"])
    print("max flow %d through graph:\n%s"%(flow, g))

    msg = minSpanningTree(g)
    print("mininum spanning tree:\n%s"%msg)

    status, ns = topoSort(g)
    print("cycle in graph: %s %s"%(status, ",".join(str(n.id) for n in ns)))

    g.remoteEdge(e12)
    status, ns = topoSort(g)
    print("order on graph: %s %s"%(status, ",".join(str(n.id) for n in ns)))

