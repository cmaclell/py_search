"""
This module contains the :class:`Node` class, which is used to represent a
state in the search, and a number of functions implementing different
strategies for conducting search search.
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division
from collections import deque
from heapq import heappush
from heapq import heappop
from heapq import heapify

class Node(object):
    """
    A class to represent a node in the search. This node stores state
    information, path to the state, cost to reach the node, depth of the node,
    and any extra information.

    :param state: the state at this node
    :type state: object for tree search and hashable object for graph search
    :param parent: the node from which the current node was generated
    :type parent: :class:`Node`
    :param action: the action performed to transition from parent to current.
    :type action: typically a string, but can be any object
    :param cost: the cost of reaching the current node
    :type cost: float
    :param depth: the distance of the current node from the initial node
    :type depth: int
    :param extra: extra information to store in this node, typically used to
    store non-hashable information about the state.
    :type extra: object
    """
    
    def __init__(self, state, parent=None, action=None, cost=0, depth=0,
                 extra=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost
        self.extra = extra

    def getSolution(self):
        """
        Returns a list of actions necessary to reach the current node from the
        initial node.
        """
        actions = []
        current = self
        while current.parent:
            actions.append(current.action)
            current = current.parent
        actions.reverse()
        return actions

    def __str__(self):
        return str(self.state) + str(self.extra)

    def __repr__(self):
        return repr(self.state)

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __ne__(self, other):
        return not self.__eq__(other)

class Fringe(object):

    def push(self, node):
        raise NotImplemented("No push method")

    def extend(self, nodes):
        for n in nodes:
            self.push(n)

    def pop(self):
        raise NotImplemented("No pop method")

    def __len__(self):
        raise NotImplemented("No len method")

class FIFOQueue(Fringe):

    def __init__(self):
        self.nodes = deque()

    def push(self, node):
        self.nodes.append(node)

    def remove(self, node):
        for i in range(self.nodes.count(node)):
            self.nodes.remove(node)

    def pop(self):
        return self.nodes.popleft()

    def __len__(self):
        return len(self.nodes)

class LIFOQueue(FIFOQueue):

    def pop(self):
        return self.nodes.pop()

class PriorityQueue(Fringe):

    def __init__(self, heuristic=None, cost_limit=None, max_length=None):
        self.nodes = []
        self.open_list = {}
        self.node_count = 0
        self.heuristic = heuristic
        self.max_length = max_length
        self.cost_limit = cost_limit

    def push(self, node):
        value = node.cost

        if self.cost_limit is not None and value > self.cost_limit:
            return

        if self.heuristic:
            value += self.heuristic(node)

        if node in self.open_list and value < self.open_list[node]:
            #print('remove from open')
            self.remove(node)
            del self.open_list[node]

        if node not in self.open_list:
            self.node_count += 1
            heappush(self.nodes,(value, self.node_count, node))

    def extend(self, nodes):
        for n in nodes:
            self.push(n)

        if self.max_length is not None and len(self.nodes) > self.max_length:
            new_nodes = []
            self.open_list = {}
            for i in range(self.max_length):
                value, count, node = heappop(self.nodes)
                heappush(new_nodes, (value, count, node))
                self.open_list[node] = value
            self.nodes = new_nodes

    def remove(self, node):
        self.nodes = [ele for ele in self.nodes if ele[2] != node]
        heapify(self.nodes)

    def pop(self):
        value, count, node = heappop(self.nodes)
        return node

    def __len__(self):
        return len(self.nodes)

def tree_search(initial, successor, goal_test, fringe):
    """
    Perform tree search using the given fringe class.

    Returns an iterators so alternative solutions can be found.
    """
    fringe.push(initial)

    while len(fringe) > 0:
        node = fringe.pop()

        if goal_test(node):
            #print("Nodes evaluated: %i" % fringe.node_count)
            yield node
        else:
            fringe.extend(successor(node))

def graph_search(initial, successor, goal_test, fringe):
    """
    Perform graph search using the given fringe class.

    Returns an iterators so alternative solutions can be found.
    """
    closed = {}
    fringe.push(initial)

    while len(fringe) > 0:
        node = fringe.pop()

        if goal_test(node):
            #print("Nodes evaluated: %i" % fringe.node_count)
            yield node
        if node not in closed:
            closed[node] = True
            fringe.extend(successor(node))

def depth_first_tree_search(initial, successor, goal_test):
    for solution in tree_search(initial, successor, goal_test, LIFOQueue()):
        yield solution

def breadth_first_tree_search(initial, successor, goal_test):
    for solution in tree_search(initial, successor, goal_test, FIFOQueue()):
        yield solution

def dijkstra_tree_search(initial, successor, goal_test):
    for solution in tree_search(initial, successor, goal_test,
                                PriorityQueue()):
        yield solution

def a_star_tree_search(initial, successor, goal_test, heuristic):
    for solution in tree_search(initial, successor, goal_test,
                                PriorityQueue(heuristic)):
        yield solution

def a_star_graph_search(initial, successor, goal_test, heuristic):
    for solution in graph_search(initial, successor, goal_test,
                                PriorityQueue(heuristic)):
        yield solution

def beam_tree_search(initial, successor, goal_test, heuristic, beam_width=1):
    for solution in tree_search(initial, successor, goal_test,
                                PriorityQueue(heuristic, max_length=beam_width)):
        yield solution

def beam_graph_search(initial, successor, goal_test, heuristic, beam_width=2):
    for solution in graph_search(initial, successor, goal_test,
                                PriorityQueue(heuristic, max_length=beam_width)):
        yield solution

def widening_beam_graph_search(initial, successor, goal_test, heuristic,
                               initial_beam_width=1, max_beam_width=1000):
    beam_width = initial_beam_width
    found = False
    while not found and beam_width <= max_beam_width:
        for solution in graph_search(initial, successor, goal_test,
                                    PriorityQueue(heuristic, max_length=beam_width)):
            found = True
            yield solution
        beam_width += 1
        #print('Increasing beam width to: %i' % beam_width)

def IDDFS(initial, successorFn, goalTestFn, initialDepthLimit=1):
    """
    Depth Limited Depth First Search
    """
    depthLimit = initialDepthLimit
    maxDepth = False
    nodeCount = 0
    successorFn = successorFn
    goalTestFn = goalTestFn

    while not maxDepth:
        maxDepth = True
        fringe = deque()
        getNext = fringe.pop
        fringe.append(initial)

        while fringe:
            current = getNext()
            nodeCount += 1
            if goalTestFn(current):
                print("Succeeded!")
                print("Nodes evaluated: %i" % nodeCount)
                yield current

            if current.depth < depthLimit:
                fringe.extend(successorFn(current))
            else:
                maxDepth = False
        depthLimit += 1
        print("Increasing depth limit to: %i" % depthLimit)

    print("Failed")
    print("Nodes evaluated: %i" % nodeCount)

def DLDFS(initial, successorFn, goalTestFn, depthLimit=float('inf')):
    """
    Depth Limited Depth First Search
    """
    fringe = deque()
    getNext = fringe.pop
    nodeCount = 0
    fringe.append(initial)
    successorFn = successorFn
    goalTestFn = goalTestFn

    while fringe:
        current = getNext()

        nodeCount += 1
        if goalTestFn(current):
            print("Succeeded!")
            print("Nodes evaluated: %i" % nodeCount)
            yield current

        if current.depth < depthLimit:
            fringe.extend(successorFn(current))

    print("Failed")
    print("Nodes evaluated: %i" % nodeCount)

def DepthFS(initial, successorFn, goalTestFn):
    """
    Depth first search
    """
    fringe = deque()
    getNext = fringe.pop
    nodeCount = 0
    fringe.append(initial)
    successorFn = successorFn
    goalTestFn = goalTestFn

    while fringe:
        current = getNext()

        nodeCount += 1
        if goalTestFn(current):
            print("Succeeded!")
            print("Nodes evaluated: %i" % nodeCount)
            yield current

        fringe.extend(successorFn(current))

    print("Failed")
    print("Nodes evaluated: %i" % nodeCount)

def DepthFGS(initial, successorFn, goalTestFn):
    """
    Depth first grid search (removes duplicates)
    """
    nodeCount = 0
    fringe = deque()
    closedList = set()
    openList = set()

    fringe.append(initial)
    openList.add(initial)

    while fringe:
        current = fringe.pop()
        openList.remove(current)
        closedList.add(current)

        if goalTestFn(current):
            #print("Succeeded!")
            #print("Nodes evaluated: %i" % nodeCount)
            yield current

        # Trick to push the looping into C execution
        added = [fringe.append(s) or openList.add(s) for s in
                 successorFn(current) if s not in closedList and s not in
                 openList]
        nodeCount += len(added)
        #for s in successorFn(current):
        #    nodeCount += 1
        #    if s not in closedList and s not in openList:
        #        fringe.append(s)
        #        openList.add(s)

    #print("Failed")
    #print("Nodes evaluated: %i" % nodeCount)

def BreadthFS(initial, successorFn, goalTestFn):
    """
    Breadth First search
    """
    nodeCount = 1
    fringe = deque()
    fringe.append(initial)

    while fringe:
        current = fringe.popleft()

        nodeCount += 1
        if goalTestFn(current):
            print("Succeeded!")
            print("Nodes evaluated: %i" % nodeCount)
            yield current

        for s in successorFn(current):
            nodeCount += 1
            fringe.append(s)

    print("Failed")
    print("Nodes evaluated: %i" % nodeCount)

def BreadthFGS(initial, successorFn, goalTestFn):
    """
    Breadth First Graph Search
    """
    nodeCount = 1
    fringe = deque()
    closedList = set()
    openList = set()
    fringe.append(initial)
    openList.add(initial)

    while fringe:
        current = fringe.popleft()
        openList.remove(current)
        closedList.add(current)

        if goalTestFn(current):
            #print("Succeeded!")
            #print("Nodes evaluated: %i" % nodeCount)
            yield current

        added = [fringe.append(s) or openList.add(s) for s in
                 successorFn(current) if s not in closedList and s not in
                 openList]
        nodeCount += len(added)
        #for s in successorFn(current):
        #    nodeCount += 1
        #    if s not in closedList and s not in openList:
        #        fringe.append(s)
        #        openList.add(s)

    #print("Failed")
    #print("Nodes evaluated: %i" % nodeCount)

def IDBFS(initial, successorFn, goalTestFn, heuristicFn,
          initialCostLimit=1, costInc=1):
    """
    Cost limited Best first search
    """
    nodeCount = 1
    successorFn = successorFn
    heuristicFn = heuristicFn
    goalTestFn = goalTestFn

    costMax = False
    costLimit = initialCostLimit

    while not costMax:
        costMax = True
        fringe = []
        openList = {}
        heappush(fringe, (0, nodeCount, initial))
        openList[initial] = 0

        while fringe:
            cost, counter, current = heappop(fringe)
            del openList[current]

            if goalTestFn(current):
                print("Succeeded!")
                print("Nodes evaluated: %i" % nodeCount)
                yield current

            for s in successorFn(current):
                nodeCount += 1
                sCost = s.cost + heuristicFn(s)
                if sCost <= costLimit:
                    if s in openList:
                        if sCost < openList[s]:
                            #fringe.remove((openList[s], s))
                            fringe = [e for e in fringe if e[2] != s]
                            heapify(fringe)
                            openList[s] = sCost
                            heappush(fringe, (sCost, nodeCount, s))
                    else:
                        openList[s] = sCost
                        heappush(fringe, (sCost, nodeCount, s))
                else:
                    costMax = False
        costLimit += costInc
        #print("Increasing cost limit to: %i" % costLimit)

    print("Failed")
    print("Nodes evaluated: %i" % nodeCount)

def CLBFS(initial, successorFn, goalTestFn, heuristicFn,
          costLimit=float('inf')):
    """
    Cost limited Best first search
    """
    nodeCount = 1

    fringe = []
    openList = {}
    heappush(fringe, (0, nodeCount, initial))
    openList[initial] = 0

    while fringe:
        cost, counter, current = heappop(fringe)
        del openList[current]

        if goalTestFn(current):
            print("Succeeded!")
            print("Nodes evaluated: %i" % nodeCount)
            yield current

        for s in successorFn(current):
            nodeCount += 1
            sCost = s.cost + heuristicFn(s)
            if sCost <= costLimit:
                if s in openList:
                    if sCost < openList[s]:
                        #fringe.remove((openList[s], len(fringe), s))
                        fringe = [e for e in fringe if e[2] != s]
        
                        heapify(fringe)
                        openList[s] = sCost
                        heappush(fringe, (sCost, nodeCount, s))
                else:
                    openList[s] = sCost
                    heappush(fringe, (sCost, nodeCount, s))
            else:
                print("Cost limit hit")

    print("Failed")
    print("Nodes evaluated: %i" % nodeCount)

def BestFS(initial, successorFn, goalTestFn, heuristicFn):
    """
    Best first search
    """
    nodeCount = 1
    fringe = []
    openList = {}
    heappush(fringe, (0, nodeCount, initial))
    openList[initial] = 0.0

    while fringe:
        cost, counter, current = heappop(fringe)
        del openList[current]

        if goalTestFn(current):
            print("Succeeded!")
            print("Nodes evaluated: %i" % nodeCount)
            yield current

        for s in successorFn(current):
            nodeCount += 1
            sCost = s.cost + heuristicFn(s)
            if s in openList:
                if sCost < openList[s]:
                    #fringe.remove((openList[s], ), s))
                    fringe = [e for e in fringe if e[2] != s]
                    heapify(fringe)
                    openList[s] = sCost
                    heappush(fringe, (sCost, nodeCount, s))
            else:
                openList[s] = sCost
                heappush(fringe, (sCost, nodeCount, s))

    print("Failed")
    print("Nodes evaluated: %i" % nodeCount)

def BestFGS(initial, successorFn, goalTestFn, heuristicFn):
    nodeCount = 1
    fringe = []
    closedList = {}
    openList = {}
    heappush(fringe, (0, nodeCount, initial))
    openList[initial] = 0.0

    while fringe:
        cost, counter, current = heappop(fringe)
        del openList[current]
        closedList[current] = cost

        if goalTestFn(current):
            #print("Succeeded!")
            print("Nodes evaluated: %i" % nodeCount)
            yield current

        for s in successorFn(current):
            nodeCount += 1
            sCost = s.cost + heuristicFn(s)
            if s in openList:
                if sCost < openList[s]:
                    fringe = [e for e in fringe if e[2] != s]
                    heapify(fringe)
                    openList[s] = sCost
                    heappush(fringe, (sCost, nodeCount, s))
            elif s in closedList:
                if sCost < closedList[s]:
                    del closedList[s]
                    openList[s] = sCost
                    heappush(fringe, (sCost, nodeCount, s))
            else:
                openList[s] = sCost
                heappush(fringe, (sCost, nodeCount, s))

    #print("Failed")
    #print("Nodes evaluated: %i" % nodeCount)

def BeamS(initial, successorFn, goalTestFn, heuristicFn, initialBeamWidth=1):
    """
    Beam Search (allows duplicates)
    """
    nodeCount = 1
    beamMax = False
    beamWidth = initialBeamWidth
    while not beamMax:
        beamMax = True
        fringe = []
        openList = {}
        heappush(fringe, (0, nodeCount, initial))
        openList[initial] = 0

        while fringe:
            cost, counter, current = heappop(fringe)

            if goalTestFn(current):
                #print("Succeeded!")
                #print("Nodes evaluated: %i" % nodeCount)
                yield current

            for s in successorFn(current):
                nodeCount += 1
                sCost = s.cost + heuristicFn(s)
                if s in openList:
                    if sCost < openList[s]:
                        #fringe.remove((openList[s], s))
                        fringe = [e for e in fringe if e[2] != s]
                        heapify(fringe)
                        openList[s] = sCost
                        heappush(fringe, (sCost, nodeCount, s))
                else:
                    openList[s] = sCost
                    heappush(fringe, (sCost, nodeCount, s))

            if len(fringe) > beamWidth:
                best = []
                openList = {}
                for i in range(beamWidth):
                    if fringe:
                        c, s = heappop(fringe)
                        openList[s] = c
                        heappush(best, (cost, nodeCount, s))
                fringe = best
                beamMax = False
        
        beamWidth += 1
        #print("Increasing beam width to: %i" % beamWidth)

    #print("Failed")
    #print("Nodes evaluated: %i" % nodeCount)

def BeamGS(initial, successorFn, goalTestFn, heuristicFn, initialBeamWidth=1):
    """
    Beam Grid Search (no duplicates)
    """
    nodeCount = 1

    beamMax = False
    beamWidth = initialBeamWidth
    while not beamMax:
        beamMax = True
        fringe = []
        openList = {}
        closedList = {}
        heappush(fringe, (0, nodeCount, initial))
        openList[initial] = 0

        while fringe:
            cost, counter, current = heappop(fringe)
            del openList[current]
            closedList[current] = cost

            if goalTestFn(current):
                #print("Succeeded!")
                print("Nodes evaluated: %i" % nodeCount)
                yield current

            for s in successorFn(current):
                nodeCount += 1
                sCost = s.cost + heuristicFn(s)
                if s in openList:
                    if sCost < openList[s]:
                        #fringe.remove((openList[s], s))
                        fringe = [e for e in fringe if e[2] != s]
                        heapify(fringe)
                        openList[s] = sCost
                        heappush(fringe, (sCost, nodeCount, s))
                elif s in closedList:
                    if sCost < closedList[s]:
                        del closedList[s]
                        openList[s] = sCost
                        heappush(fringe, (sCost, nodeCount, s))
                else:
                    openList[s] = sCost
                    heappush(fringe, (sCost, nodeCount, s))

            if len(fringe) > beamWidth:
                best = []
                openList = {}
                for i in range(beamWidth):
                    if fringe:
                        c, count, s = heappop(fringe)
                        openList[s] = c
                        heappush(best, (c, count, s))
                fringe = best
                beamMax = False
        
        beamWidth += 1
        print("Increasing beam width to: %i" % beamWidth)

    print("Failed")
    print("Nodes evaluated: %i" % nodeCount)
