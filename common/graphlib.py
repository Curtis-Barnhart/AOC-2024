#!python3

import heapq

MAX_NODES = 1000000

# see: https://memgraph.com/blog/graph-algorithms-applications


# classes:
#   Graph
#       -- create
#       def newNode(self, id=None, dedup=False):
#       def newEdge(self, nStart, nEnd, id=None, wgt=1, dedup=False):
#       def removeEdge(self, e):
#       -- sub-graph
#       def newSubGraph(self):
#       def cpNode(self, nParent):
#       def cpEdge(self, eParent):
#       def cpAllEdges(self):
#       -- data
#       id
#       isDirected: undirected graphs have two directed nodes created in the graph
#       ns: dict from Node.id to Node
#       es: dict from Edge.id to Edge
#   Node
#       -- data
#       id
#       esOut: dict from end Node.id to outgoing edges
#       esIn: dict from start Node.id to incoming edges
#   Edge
#       -- data
#       id
#       nStart
#       nEnd
#       wgt
#       flow: output from maxFlowGraph
#
# classes when using sub-graphs:
#   Graph (that contains a sub-graph)
#       gParent: the graph that this graph is a sub-graph of
#       esBoundary: list of BoundaryEdge (check ExitEdge.isDel)
#               edges having one node in and one node out of the sub-graph
#   BoundaryEdge
#       -- copied from nParent
#       id
#       nStart
#       nEnd
#       wgt
#       -- additional
#       nParent: the node in gParent that this edge connects to, either nStart or nEnd
#       isDel: should this edge been removed from this list
#
# funcs:
#   shortestWgt(g, nStart, nEnd)
#       (un)directed
#   longestWgt(g, nStart, nEnd)
#       (un)directed
#   maxFlowPath(g, nStart, nEnd)
#       (un)directed
#   maxFlowGraph(g, nStart, nEnd)
#       (un)directed
#   minSpanningTrees(g)
#       undirected
#   allSubGraphs(g)
#       undirected
#   topoSort(g)
#       directed
#   depthFirstSearch(g, nStart, fFirstVisit, fSecondVisit, fParent, fCycleVisit)
#       directed
#       use DFS_createTreeSumFuncs to create the 4 functions
#
# missing:
#   def connectedComponents(g):
#       https://stackoverflow.com/questions/37291876/finding-fully-connected-components
#   def eulerCircuit(g):
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

    def _getBackPath(self, l=None):
        "returns a list of ids"
        if l == None:
            l = []
        if self._back:
            self._back._getBackPath(l)
        l.append(self.id)
        return l

    def __lt__(self, other):
        return self._order_by < other._order_by

    def __str__(self):
        return self.nStr([])

    def nStr(self, showWhat):
        s = ""
        if "back" in showWhat and self._back != None:
            s = " back %d"%self._back.id
        if "nodewgt" in showWhat and self._back != None:
            s += " wgt %d"%self.wgt
        return "Node(%s) in(%s) out(%s)%s"%(
            self.id,
            # things coming in, show the nStarting node
            ",".join(str(e.nStart.id) for e in self.esIn.values()),
            # things going out, show the nEnd node
            ", ".join(
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
        ss.append("%s"%self.nEnd.id)
        if "flow" in showWhat:
            ss.append("flow %d of %d"%(self.flow, self.wgt))
        elif "edgewgt" in showWhat:
            ss.append("wgt %d"%self.wgt)
        return " ".join(ss)

    def __str__(self):
        return "Edge(%s)"%self.id

class BoundaryEdge(object):
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
        return "BoundaryEdge(%s to %s wgt %d parent_is %s)"%(self.nStart.id, self.nEnd.id, self.wgt, self.nParent.id)

class Graph(object):
    ###############################
    # creation
    ###############################

    gid = -1;

    def _nextId():
        Node.gid += 1
        return Node.gid

    def __init__(self, isDirected=True):
        self.id = Graph._nextId()       # unique id
        self.ns = {}                    # dict from Node.id to Node
        self.es = {}                    # dict from Edge.id to Edge
        self.isDirected = isDirected    # undirected graphs have two directed nodes created in the graph
        self._showWhat = set()

        # used for sub-graphs
        self.esBoundary = None
        self.gParent = None

    def getNode(self, id):
        return self.ns.get(id, None)

    def newNode(self, id=None, dedup=False):
        if id in self.ns:
            if dedup:
                return self.ns[id]
            else:
                print("ERROR: duplicate node")
                return None
        node = Node(id)
        self.ns[node.id] = node
        return node

    def newEdge(self, nStart, nEnd, id=None, wgt=1, dedup=False):
        if id in self.es:
            if dedup:
                return self.es[id]
            else:
                print("ERROR: duplicate edge")
                return None
        edge = Edge(nStart, nEnd, id, wgt)
        self.es[edge.id] = edge
        if not self.isDirected:
            if id:
                id = id + MAX_NODES
            edge = Edge(nEnd, nStart, id, wgt)
            self.es[edge.id] = edge
        return edge

    def removeEdge(self, e):
        del e.nStart.esOut[e.nEnd.id]
        del e.nEnd.esIn[e.nStart.id]
        del self.es[e.id]
        if self.gParent:
            # TODO: if this is a sub-graph, things must be adjusted
            pass

    ###############################
    # Sub graphs
    ###############################

    def newSubGraph(self):
        sg = Graph(isDirected = self.isDirected)
        sg.gParent = self
        sg.esBoundary = []
        return sg

    def cpNode(self, nParent):
        if nParent.id in self.ns:
            print("ERROR: cp node already copied")
            return

        nNew = self.newNode(nParent.id)

        for be in self.esBoundary:
            if (be.nStart.id in self.ns) ^ (be.nEnd.id in self.ns):
                be.isDel = True

        for e in nParent.esOut.values():
            if e.nEnd.id not in self.ns:
                if e not in self.esBoundary:
                    # include in esBoundary
                    xNew = BoundaryEdge(e, e.nEnd)
                    heapq.heappush(self.esBoundary, xNew)

        for e in nParent.esIn.values():
            if e.nStart.id not in self.ns:
                if e not in self.esBoundary:
                    # include in esBoundary
                    xNew = BoundaryEdge(e, e.nStart)
                    heapq.heappush(self.esBoundary, xNew)

    def cpEdge(self, eParent):
        if not self.gParent:
            print("ERROR: not a sub-graph")
            return

        "copy one edge in the parent graph to this sub-graph"
        if eParent.id in self.es:
            print("ERROR: cp edge already copied")
            return

        nEdgeStart = self.ns[eParent.nStart.id]
        nEdgeEnd = self.ns[eParent.nEnd.id]

        eNew = self.newEdge(nEdgeStart, nEdgeEnd, id=eParent.id, wgt=eParent.wgt)
        eParent = self.gParent.es[eParent.id]

    def cpAllEdges(self):
        "copy all edges from the parent graph to this sub-graph"
        if not self.gParent:
            print("ERROR: not a sub-graph")
            return

        for nId in self.ns:
            for eParent in self.gParent.ns[nId].esOut.values():
                if eParent.id not in self.es:
                    self.cpEdge(eParent)

    ###############################
    # stringify
    ###############################

    def setShow(self, value):
        """
        back - show back propogation on nodes
        flow - show flow on edges
        edgewgt - show wgt on edges
        nodewgt - show wgt on edges
        """
        self._showWhat = set(value)

    def __str__(self):
        l = []
        for n in self.ns.values():
            l.append("    " + n.nStr(self._showWhat))
        if self.esBoundary:
            l.append("    sub-graph boundary: " + ", ".join(str(e) for e in self.esBoundary if not e.isDel))
        return "\n".join(l)

    ###############################
    # internal
    ###############################

    def _unvisitNodes(self):
        for n in self.ns.values():
            n.visited1 = False
            n.visited2 = False
            n._back = None

    def _zeroEdgeFlow(self):
        for e in self.es.values():
            e.flow = 0


def maxFlowPath(g, nStart, nEnd):
    """
    returns (smallest wgt-flow along the path, list of nodes along the path)
    returns None if no path exists with all edges having wgt-flow greater than 0
    """
    g._unvisitNodes()
    nStart._order_by = -1e200
    nStart.visited1 = True
    heap = [nStart]
    while heap:
        # get smallest weighted node in the heap
        nEdgeStart = heapq.heappop(heap)
        if nEdgeStart.id == nEnd.id:
            return (-nEdgeStart._order_by, nEdgeStart._getBackPath())
        for e in nEdgeStart.esOut.values():
            nEdgeEnd = e.nEnd
            if nEdgeEnd.id != nStart.id:
                edgeFlow = min(e.wgt-e.flow, -nEdgeStart._order_by)
                if edgeFlow > 0:
                    maxWgt = max(nEdgeStart._order_by, -edgeFlow)
                    if not nEdgeEnd.visited1 or nEdgeEnd._order_by < maxWgt:
                        nEdgeEnd._back = nEdgeStart
                        nEdgeEnd._order_by = maxWgt
                        nEdgeEnd.visited1 = True
                        heapq.heappush(heap, nEdgeEnd)

def shortestWgt(g, nStart, nEnd, byEdgeCount=False):
    g._unvisitNodes()
    nStart._order_by = 0
    nStart.visited1 = True
    heap = [nStart]
    while heap:
        # get smallest weighted node in the heap
        nEdgeStart = heapq.heappop(heap)
        if nEdgeStart.id == nEnd.id:
            return (nEdgeStart._order_by, nEdgeStart._getBackPath())
        for e in nEdgeStart.esOut.values():
            nEdgeEnd = e.nEnd
            pathWgt = nEdgeStart._order_by + (1 if byEdgeCount else e.wgt)
            if not nEdgeEnd.visited1 or nEdgeEnd._order_by > pathWgt:
                nEdgeEnd._back = nEdgeStart
                nEdgeEnd._order_by = pathWgt
                nEdgeEnd.visited1 = True
                heapq.heappush(heap, nEdgeEnd)

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
    returns (status, list of node)
    where status is one of "CYCLE", "ORDER", or "UNDIRECTED"
    """
    if not g.isDirected:
        return ("UNDIRECTED", [])

    g._unvisitNodes()
    order = []
    for n in g.ns.values():
        cycle = _topoSort(order, n)
        if cycle:
            cycle.reverse()
            return ("CYCLE", cycle)
    order.reverse()
    return ("ORDER", order)

def _longHardWay(nStart, nEnd, pathWgt, byEdgeCount):
    nStart.visited1 = True
    oldLong = None
    for e in nStart.esOut.values():
        nxt = e.nEnd
        if nxt.id == nEnd.id:
            nxt._back = nStart
            newLong = (pathWgt + (1 if byEdgeCount else e.wgt), nxt._getBackPath())
        elif not nxt.visited1:
            nxt._back = nStart
            newLong = _longHardWay(nxt, nEnd, pathWgt + (1 if byEdgeCount else e.wgt), byEdgeCount)
        else:
            continue
        if newLong and (not oldLong or oldLong[0] < newLong[0]):
            oldLong = newLong
    nStart.visited1 = False
    return oldLong

def longestWgt(g, nStart, nEnd, byEdgeCount=False):
    status, ts = topoSort(g)
    if status == "ORDER":
        g._unvisitNodes()
        findStart = False
        for n in ts:
            if not findStart:
                if n.id == nStart.id:
                    n._order_by = 0
                    n.visited1 = True
                    n._back = None
                    findStart = True
            elif n.id == nEnd.id:
                return (n._order_by, n._getBackPath())
            if findStart:
                for e in n.esOut.values():
                    wgt = n._order_by + (1 if byEdgeCount else e.wgt)
                    if not e.nEnd.visited1 or e.nEnd._order_by < wgt:
                        e.nEnd._order_by = wgt
                        e.nEnd._back = n
                        e.nEnd.visited1 = True
    else:
        g._unvisitNodes()
        nStart._order_by = 0
        nStart._back = None
        return _longHardWay(nStart, nEnd, 0, byEdgeCount)

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

def minSpanningTrees(g):
    gs = []
    ns = set(id for id in g.ns)
    while ns:
        gSub = g.newSubGraph()
        gs.append(gSub)
        n = g.ns[next(n for n in ns)]
        gSub.cpNode(n)
        while gSub.esBoundary:
            be = heapq.heappop(gSub.esBoundary)
            if be.isDel:
                continue

            gSub.cpNode(be.nParent)
            gSub.cpEdge(be)
        ns.difference_update(id for id in gSub.ns)
    return gs

def allSubGraphs(g):
    gs = minSpanningTrees(g)
    for g in gs:
        g.cpAllEdges()
    return gs

####################
# depth first search
####################

def _depthFirstSearch(g, eParent, nStart, fFirstVisit, fSecondVisit, fParent, fCycleVisit):
    nStart._back = eParent.nStart if eParent else None
    nStart.visited1 = True
    childValues = []
    for e in nStart.esOut.values():
        nChild = e.nEnd
        if nChild.visited1:
            value = fSecondVisit(e, nChild) if nChild.visited2 else fCycleVisit(e, nChild)
            if value != None:
                childValues.append(value)
        else:
            value = _depthFirstSearch(g, e, nChild, fFirstVisit, fSecondVisit, fParent, fCycleVisit)
            if value != None:
                childValues.append(value)
    answer = fParent(eParent, nStart, childValues) if childValues else fFirstVisit(eParent, nStart)
    nStart.visited2 = True
    return answer

def depthFirstSearch(g, nStart, fFirstVisit, fSecondVisit, fParent, fCycleVisit):
    """
    depth first search starting at nStart
    each leaf in the search is given the value fFirstVisit(edge-to-that-node, that-node)
    each node visited a second time,
        having previously been called with fFirstVisit or fParent,
        is given the value fSecondVisit(edge-to-that-node, that-node)
    each node visited a second time,
        having not previously been called with any function due to a cycle,
        is given the value fCycleVisit(edge-to-that-node, that-node)
    each node with child nodes is given the value fParent(edge-to-that-node, that-node, list of child values)
    """
    g._unvisitNodes()
    return _depthFirstSearch(g, None, nStart, fFirstVisit, fSecondVisit, fParent, fCycleVisit)

def DFS_createTreeSumFuncs_dbg(fNodeWgt, fEdgeWgt, multiVisit=True, debug=False):

    def fFirstVisit(e, n):
        n.wgt = fNodeWgt(n,True)
        eWgt = fEdgeWgt(e,n)
        return (eWgt, n.id, n.wgt)

    def fSecondVisit(e, n):
        eWgt = fEdgeWgt(e,n) if multiVisit else 0
        return (eWgt, n.id, n.wgt)

    def fParent(e, n, values):
        nWgt = fNodeWgt(n,False)
        n.wgt = sum(v[0] for v in values) + nWgt
        eWgt = fEdgeWgt(e,n) if e else n.wgt
        return (eWgt, n.id, values)

    def fCycleVisit(e, n):
        raise Exception("CYCLE")

    return [
        fFirstVisit,
        fSecondVisit,
        fParent,
        fCycleVisit]

def DFS_createTreeSumFuncs(fNodeWgt, fEdgeWgt, multiVisit=True, debug=False):
    """
    fNodeWgt(n, isLeaf): gives each node a weight
    fEdgeWgt(e, n): gives the traversal of an edge a weight

    each node's weight its base weight + sum of all its children's wgts times the edge wgt

    multiVisit: if true, only the first visit of a node adds to the total score
    """

    def fFirstVisit(e, n):
        n.wgt = fNodeWgt(n,True)
        return fEdgeWgt(e,n)

    def fSecondVisit(e, n):
        return fEdgeWgt(e,n) if multiVisit else 0

    def fParent(e, n, values):
        n.wgt = sum(values) + fNodeWgt(n,False)
        return fEdgeWgt(e,n) if e else n.wgt

    def fCycleVisit(e, n):
        raise Exception("CYCLE")

    return [
        fFirstVisit,
        fSecondVisit,
        fParent,
        fCycleVisit]

if __name__ == "__main__":
    g = Graph(isDirected=True)
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

    n4 = g.newNode()
    n5 = g.newNode()
    n6 = g.newNode()
    g.newEdge(n4,n5,wgt=30)
    g.newEdge(n6,n5,wgt=20)
    g.newEdge(n4,n6,wgt=10)

    short_path = shortestWgt(g, n0, n3)
    print("short: %s"%repr(short_path))

    long_path = longestWgt(g, n0, n3)
    print("long by wgt: %s"%repr(long_path))
    long_path = longestWgt(g, n0, n3, byEdgeCount=True)
    print("long by edge count: %s"%repr(long_path))

    flow = maxFlowGraph(g, n0, n3)
    g.setShow(["flow"])
    print("max flow %d through graph:\n%s"%(flow, g))

    gsMinSpan = minSpanningTrees(g)
    for g0 in gsMinSpan:
        print("sub-graph %s"%g0.id)
        print("  mininum spanning tree:\n%s"%g0)
        g0.cpAllEdges()
        print("  sub-graph:\n%s"%g0)
        status, ns = topoSort(g0)
        print("  order on sub-graph: %s %s"%(status, ",".join(str(n.id) for n in ns)))

    status, ns = topoSort(g)
    print("cycle in graph: %s %s"%(status, ",".join(str(n.id) for n in ns)))

    g.removeEdge(e12)
    status, ns = topoSort(g)
    print("order on graph: %s %s"%(status, ",".join(str(n.id) for n in ns)))

