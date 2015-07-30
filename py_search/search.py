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
from tabulate import tabulate
import uuid

class Problem(object):
    """
    A problem to solve.
    """
    def __init__(self, initial, extra=None):
        self.initial = Node(initial, extra=extra)

    def successor(self, node):
        raise NotImplemented("No successor function implemented")

    def goal_test(self, node):
        raise NotImplemented("No goal test function implemented")

class AnnotatedProblem(Problem):
    """
    A Problem class that wraps around another Problem and keeps stats on nodes
    expanded and goal tests performed.
    """
    def __init__(self, problem):
        self.problem = problem
        self.initial = problem.initial
        self.nodes_expanded = 0
        self.goal_tests = 0

    def successor(self, node):
        for s in self.problem.successor(node):
            self.nodes_expanded += 1
            yield s

    def goal_test(self, node):
        self.goal_tests += 1
        return self.problem.goal_test(node)

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
    
    def __init__(self, state, parent=None, action=None, cost=0, value=0,
                 depth=0, extra=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost
        self.value = value
        self.extra = extra
        self.uuid = uuid.uuid4()

    def path(self):
        """
        Returns a path (tuple of actions) from the initial to current node.
        """
        actions = []
        current = self
        while current.parent:
            actions.append(current.action)
            current = current.parent
        actions.reverse()
        return tuple(actions)

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

    def __lt__(self, other):
        """
        Used for sorting
        """
        return (self.value, self.uuid) < (other.value, other.uuid)


class Fringe(object):
    """
    A template for a fringe class. Used to control the strategy of different
    search approaches.
    """

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
    """
    A first-in-first-out queue. Used to get breadth first search behavior.
    """

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
    """
    A last-in-first-out queue. Used to get depth first search behavior.
    """

    def pop(self):
        return self.nodes.pop()

class PrioritySet(Fringe):
    """
    A priority set that sorts elements by their value.
    """

    def __init__(self, cost_limit=None, max_length=None):
        self.nodes = []
        self.open_list = {}
        self.node_count = 0
        self.max_length = max_length
        self.cost_limit = cost_limit

    def push(self, node):
        if self.cost_limit is not None and node.value > self.cost_limit:
            return

        if node in self.open_list and node.value < self.open_list[node]:
            self.remove(node)

        if node not in self.open_list:
            self.node_count += 1
            heappush(self.nodes, node)
            self.open_list[node] = node.value

    def extend(self, nodes):
        for n in nodes:
            self.push(n)

        if self.max_length is not None and len(self.nodes) > self.max_length:
            new_nodes = []
            new_open_list = {}
            for i in range(self.max_length):
                node = heappop(self.nodes)
                heappush(new_nodes, node)
                new_open_list[node] = node.value
            self.nodes = new_nodes
            self.open_list = new_open_list

    def remove(self, node):
        self.nodes = [ele for ele in self.nodes if ele != node]
        del self.open_list[node]
        heapify(self.nodes)

    def pop(self):
        node = heappop(self.nodes)
        del self.open_list[node]
        return node

    def __len__(self):
        return len(self.nodes)

def tree_search(problem, fringe):
    """
    Perform tree search using the given fringe class.

    Returns an iterators so alternative solutions can be found.
    """
    fringe.push(problem.initial)

    while len(fringe) > 0:
        node = fringe.pop()

        if problem.goal_test(node):
            yield node
        else:
            fringe.extend(problem.successor(node))

def graph_search(problem, fringe):
    """
    Perform graph search using the given fringe class.

    Returns an iterators so alternative solutions can be found.
    """
    closed = {}
    fringe.push(problem.initial)

    while len(fringe) > 0:
        node = fringe.pop()

        if problem.goal_test(node):
            yield node

        if node not in closed or node.value < closed[node]:
            closed[node] = node.value
            fringe.extend(problem.successor(node))

def depth_first_search(problem, search=graph_search):
    for solution in search(problem, LIFOQueue()):
        yield solution

def breadth_first_search(problem, search=graph_search):
    for solution in search(problem, FIFOQueue()):
        yield solution

def best_first_search(problem, search=graph_search, cost_limit=float('inf')):
    for solution in search(problem, PrioritySet(cost_limit=cost_limit)):
        yield solution

def iterative_deepening_best_first_search(problem, search=graph_search,
                                          initial_cost_limit=0, cost_inc=1,
                                          max_cost_limit=float('inf')): 

    cost_limit = initial_cost_limit
    while cost_limit < max_cost_limit:
        for solution in search(problem, PrioritySet(cost_limit=cost_limit)):
            yield solution
        cost_limit += cost_inc
        print("%s - increasing cost_limit to: %i" % (__name__, cost_limit))

def beam_search(problem, search=graph_search, beam_width=1):
    for solution in search(problem, PrioritySet(max_length=beam_width)):
        yield solution

def widening_beam_search(problem, search=graph_search, initial_beam_width=1,
                         max_beam_width=1000):
    beam_width = initial_beam_width
    while beam_width <= max_beam_width:
        for solution in search(problem, PrioritySet(max_length=beam_width)):
            yield solution
        beam_width += 1
        print("%s - widening beam width to: %i" % (__name__, beam_width))

def compare_searches(problems, searches):
    table = []

    for problem in problems:
        for search in searches:
            annotated_problem = AnnotatedProblem(problem)
            sol = next(search(annotated_problem))

            value = "Failed"
            if sol:
                value = sol.value

            table.append([problem.__class__.__name__, search.__name__,
                          annotated_problem.goal_tests,
                          annotated_problem.nodes_expanded, value])

    print(tabulate(table, headers=['Problem', 'Search Alg', 'Goal Tests',
                                   'Nodes Expanded', 'Solution Value'],
                   tablefmt="fancy_grid"))
