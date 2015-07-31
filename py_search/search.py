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
from blist import sortedlist
from tabulate import tabulate
import uuid

class Problem(object):
    """
    A problem to solve.
    """
    def __init__(self, initial, extra=None):
        self.initial = Node(initial, extra=extra)

    def node_value(self, node):
        """
        The value of the node that is minimized by the search. By default the
        path_cost is used, but a heuristic could be added here.
        """
        return node.cost()

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
        self.nodes_evaluated = 0

    def node_value(self, node):
        """
        A wraper for the node value method that keeps track of the number of
        times a node value was calculated.
        """
        self.nodes_evaluated += 1
        return self.problem.node_value(node)

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
    
    def __init__(self, state, parent=None, action=None, path_cost=0,
                 extra=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.extra = extra
        self.uuid = uuid.uuid4()

    def depth(self):
        """
        Returns the depth of the current node. Uses a loop to compute depth
        (recursive calls are weird in python).
        """
        curr = self
        depth = 0
        while curr.parent is not None:
            curr = curr.parent
            depth += 1
        return depth

    def cost(self):
        """
        Returns the cost of the current node. 
        """
        return self.path_cost

    def update_path(self, other):
        """
        Update the path the the current node with another nodes path.
        Specificially, this updates the parent, action, and action_cost.
        """
        self.parent = other.parent
        self.action = other.action
        self.path_cost = other.path_cost

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
        return self.uuid < other.uuid

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
    A priority set that sorts elements by their value. Always returns the
    minimum value item. When a duplicate node is added the one with the minimum
    value is kept. A :class:`PrioritySet` accepts a node_value function, a
    cost_limit (nodes with a value greater than this limit will not be added)
    and a max_length parameter. If adding an item ever causes the size to
    exceed the max_length then the worst nodes are removed until the list is
    equal to max_length.

    >>> pq = PrioritySet()
    >>> n1 = Node(1, path_cost=1)
    >>> n3 = Node(3, path_cost=3)
    >>> n7 = Node(7, path_cost=7)

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

    def __init__(self, node_value=lambda x: x.cost(), cost_limit=None,
                 max_length=float('inf')):
        self.nodes = sortedlist()
        self.open_list = {}
        self.max_length = max_length
        self.cost_limit = cost_limit
        self.node_value = node_value

    def push(self, node):
        """
        Push a node into the priority queue.
        """
        value = self.node_value(node)

        if self.cost_limit is not None and value > self.cost_limit:
            return

        if node in self.open_list and value > self.open_list[node][0]:
            return

        if node in self.open_list:
            self.nodes.remove(self.open_list[node])
            del self.open_list[node]

        self.nodes.add((value, node))
        self.open_list[node] = (value, node)

        if len(self.nodes) > self.max_length:
            val, node = self.nodes.pop()
            del self.open_list[node]

    def pop(self):
        val, node = self.nodes.pop(0)
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
        closed[node] = node

        if problem.goal_test(node):
            yield node
        else:
            for s in problem.successor(node):
                if s in closed and s.cost() < closed[node].cost():
                    closed[node].update(s)
                if s not in closed:
                    fringe.push(s)

def depth_first_search(problem, search=graph_search):
    for solution in search(problem, LIFOQueue()):
        yield solution

def breadth_first_search(problem, search=graph_search):
    for solution in search(problem, FIFOQueue()):
        yield solution

def best_first_search(problem, search=graph_search, cost_limit=float('inf')):
    for solution in search(problem, PrioritySet(node_value=problem.node_value,
                                                  cost_limit=cost_limit)):
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
        for solution in search(problem, PrioritySet(cost_limit=cost_limit,
                                                      node_value=problem.node_value)):
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
    for solution in search(problem, PrioritySet(node_value=problem.node_value,
                                                  max_length=beam_width)):
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
        for solution in search(problem, PrioritySet(node_value=problem.node_value,
                                                      max_length=beam_width)):
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
                value = sol.cost()

            table.append([problem.__class__.__name__, search.__name__,
                          annotated_problem.goal_tests,
                          annotated_problem.nodes_evaluated, value])

    print(tabulate(table, headers=['Problem', 'Search Alg', 'Goal Tests',
                                   'Nodes Evaluated', 'Solution Cost'],
                   tablefmt="fancy_grid"))
