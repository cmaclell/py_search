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
            print('remove from open')
            self.remove(node)
            del self.open_list[node]

        if node not in self.open_list:
            self.node_count += 1
            heappush(self.nodes,(value, self.node_count, node))

    def extend(self, nodes):
        for n in nodes:
            self.push(n)

        if self.max_length is not None and len(self.nodes) > self.max_length:
            nodes = []
            for i in range(self.max_length):
                heappush(nodes, heappop(self.nodes))
            self.nodes = nodes

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
            print(fringe.node_count)
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

def beam_graph_search(initial, successor, goal_test, heuristic, beam_width=1):
    for solution in graph_search(initial, successor, goal_test,
                                PriorityQueue(heuristic, max_length=beam_width)):
        yield solution

def widening_beam_graph_search(initial, successor, goal_test, heuristic,
                               initial_beam_width=3,
                               max_beam_width=float('inf')):
    beam_width = initial_beam_width
    found = False
    while not found and beam_width <= max_beam_width:
        for solution in graph_search(initial, successor, goal_test,
                                    PriorityQueue(heuristic, max_length=beam_width)):
            found = True
            yield solution
        beam_width += 1
