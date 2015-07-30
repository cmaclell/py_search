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
        """
        A wrapper for the successor method that keeps track of the number of
        nodes expanded.
        """
        for s in self.problem.successor(node):
            self.nodes_expanded += 1
            yield s

    def goal_test(self, node):
        """
        A wrapper for the goal_test method that keeps track of the number of
        goal_tests performed.
        """
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
    :param extra: extra information to store in this node, typically used to store non-hashable information about the state.
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
        Used for sorting.
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

    >>> fifo = FIFOQueue()
    >>> fifo.push(1)
    >>> fifo.push(2)
    >>> fifo.push(3)
    >>> print(fifo.pop())
    1
    >>> print(fifo.pop())
    2
    >>> print(fifo.pop())
    3
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

    >>> lifo = LIFOQueue()
    >>> lifo.push(1)
    >>> lifo.push(2)
    >>> lifo.push(3)
    >>> print(lifo.pop())
    3
    >>> print(lifo.pop())
    2
    >>> print(lifo.pop())
    1
    """

    def pop(self):
        return self.nodes.pop()

class PrioritySet(Fringe):
    """
    A priority set that sorts elements by their value. Sorts items lowest to
    hightest (i.e., always returns lowest value item).  
    
    This is similiar to Priority Queue, but does not allow duplicates
    (according to hash value). If a duplicate is pushed, then the lowest value
    one is kept.

    >>> pq = PrioritySet()
    >>> n1 = Node(1, value=1)
    >>> n3 = Node(3, value=3)
    >>> n7 = Node(7, value=7)

    >>> pq.push(n7)
    >>> pq.push(n1)
    >>> pq.push(n3)
    >>> pq.push(n7)

    >>> print(len(pq))
    3
    >>> print(pq.pop().state)
    1
    >>> print(pq.pop().state)
    3
    >>> print(pq.pop().state)
    7
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
    Perform tree search (i.e., search where states might be duplicated) using
    the given fringe class.

    Returns an iterators to the solutions, so more than one solution can be
    found.
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
    Perform graph search (i.e., no duplicate states) using the given fringe
    class.

    Returns an iterators to the solutions, so more than one solution can be
    found.
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
    """
    A variant of iterative deepening that uses cost to determine the limit for
    expansion. If the cost of each action has a uniform cost of 1 and there is
    no heuristic than this will give reduce to an increasing depth limited
    search. However, in situations where actions have varying costs and
    heuristic information is provide this might yield more complicated
    behavior.
    """
    cost_limit = initial_cost_limit
    while cost_limit < max_cost_limit:
        for solution in search(problem, PrioritySet(cost_limit=cost_limit)):
            yield solution
        cost_limit += cost_inc

def beam_search(problem, search=graph_search, beam_width=1):
    """
    Similar to best first search, but only maintains a limited number of nodes
    in the fringe (set by beam_width). If you have a beam_width of 1, then this
    is basically greedy hill climbing search. However, as beam width is
    increased the search becomes less and less greedy. If beam_width is set to
    float('inf') then this is equivelent to best_first_search.
    """
    for solution in search(problem, PrioritySet(max_length=beam_width)):
        yield solution

def widening_beam_search(problem, search=graph_search, initial_beam_width=1,
                         max_beam_width=1000):
    """
    A variant of beam search that successively increases the beam width. This
    is similar to iterative deepening search in that it adapts to the
    complexity of the task. It basically provides a greedy search that on
    failure becomes less greedy until it can find a solution.
    """
    beam_width = initial_beam_width
    while beam_width <= max_beam_width:
        for solution in search(problem, PrioritySet(max_length=beam_width)):
            yield solution
        beam_width += 1

def compare_searches(problems, searches):
    """
    A function for comparing different search algorithms on different problems.

    :param problems: problems to solve.
    :type problems: typically a list of problems, but could be an iterator
    :param searches: search algorithms to use.
    :type searches: typically a list of search functions, but could be an iterator
    """
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
