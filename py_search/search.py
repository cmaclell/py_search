"""
This module contains the :class:`Node` class, which is used to represent a
state in the search, and a number of functions implementing different
strategies for conducting search search.
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from math import exp
from math import pow
from math import log
from random import random

from collections import deque
from blist import sortedlist
from tabulate import tabulate

class Problem(object):
    """
    A problem to solve.
    """
    def __init__(self, initial, parent=None, action=None, initial_cost=0,
                 extra=None):
        self.initial = Node(initial, parent, action, initial_cost, extra=extra)

    def node_value(self, node):
        """
        The value of the node that is minimized by the search. By default the
        path_cost is used, but a heuristic could be added here.
        """
        return node.cost()

    def successors(self, node):
        raise NotImplemented("No successors function implemented")

    def goal_test(self, node):
        raise NotImplemented("No goal test function implemented")

class OptimizationProblem(Problem):

    def random_successor(self, node):
        raise NotImplemented("No random successor implemented!")

    def goal_test(self, node):
        raise Exception("Optimization problems do not have strict goal tests, use another search algorithm that does not utilize goal test.")

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

    def random_successor(self, node):
        """
        A wrapper for the random_successor method that keeps track of the
        number of nodes expanded.
        """
        self.nodes_expanded += 1
        return self.problem.random_successor(node)

    def node_value(self, node):
        """
        A wraper for the node value method that keeps track of the number of
        times a node value was calculated.
        """
        self.nodes_evaluated += 1
        return self.problem.node_value(node)

    def successors(self, node):
        """
        A wrapper for the successor method that keeps track of the number of
        nodes expanded.
        """
        for s in self.problem.successors(node):
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
    :param path_cost: the cost of reaching the current node
    :type path_cost: float
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
        return self.path_cost < other.path_cost

class Fringe(object):
    """
    A template for a fringe class. Used to control the strategy of different
    search approaches.
    """

    def push(self, node):
        """
        Adds one node to the collection.
        """
        raise NotImplemented("No push method")

    def extend(self, nodes):
        """
        Given an iterator (`nodes`) adds all the nodes to the collection.
        """
        for n in nodes:
            self.push(n)

    def pop(self):
        """
        Pops a node off the collection.
        """
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

    :param node_value: The node evaluation function (defaults to `lambda x:
        x.cost()`)
    :type node_value: a function with one parameter for node
    :param cost_limit: the maximum value for elements in the set, if an item
        exceeds this limit then it will not be added (defaults to
        `float('inf')) 
    :type cost_limit: float
    :param max_length: The maximum length of the list (defaults to
        `float('inf')`
    :type max_length: int or `float('inf')`
    """
    def __init__(self, node_value=lambda x: x.cost(), cost_limit=float('inf'),
                 max_length=float('inf')):
        self.nodes = sortedlist()
        self.open_list = {}
        self.max_length = max_length
        self.cost_limit = cost_limit
        self.node_value = node_value

    def peek_value(self):
        """
        Returns the value of the best node.
        """
        return self.nodes[0][0]

    def push(self, node):
        """
        Push a node into the priority set. If the node exceeds the cost limit
        then it is not added. If the node already exists in the set, then
        compare the value of the new node to the old one and keep the better
        one (the other is discarded). Finally, if the max_length is exceeded by
        adding the node, then the worst node is discarded from the set. 
        """
        value = self.node_value(node)

        if value > self.cost_limit:
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
        """
        Pop the best value from the priority queue.
        """
        val, node = self.nodes.pop(0)
        del self.open_list[node]
        return node

    def __len__(self):
        return len(self.nodes)

def tree_search(problem, fringe):
    """
    Perform tree search (i.e., search where states might be duplicated) using
    the given fringe class.Returns an iterators to the solutions, so more than
    one solution can be found.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param fringe: The fringe class to use.
    :type fringe: :class:`fringe`
    """
    fringe.push(problem.initial)

    while len(fringe) > 0:
        node = fringe.pop()

        if problem.goal_test(node):
            yield node
        else:
            fringe.extend(problem.successors(node))

def graph_search(problem, fringe):
    """
    Perform graph search (i.e., no duplicate states) using the given fringe
    class. Returns an iterator to the solutions, so more than one solution can
    be found.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param fringe: The fringe class to use.
    :type fringe: :class:`fringe`
    """
    closed = {}
    fringe.push(problem.initial)

    while len(fringe) > 0:
        node = fringe.pop()
        closed[node] = True

        if problem.goal_test(node):
            yield node
        else:
            for s in problem.successors(node):
                if s not in closed:
                    fringe.push(s)

def beam_search(problem, beam_width=1):
    """
    A variant of breadth first search where all nodes in the fringe
    are expanded, but the resulting new fringe is limited to have length
    beam_width, where the nodes with the worst value are dropped. The default
    beam width is 1, which yields greedy best-first search.

    There are different ways to implement beam search, namely best-first
    beam search and breadth-first beam search. According to:

        Wilt, C. M., Thayer, J. T., & Ruml, W. (2010). A comparison of
        greedy search algorithms. In Third Annual Symposium on Combinatorial
        Search.

    breadth-first beam search almost always performs better. They find that
    allowing the search to re-expand duplicate nodes if they have a lower cost
    improves search performance. Thus, our implementation is a breadth-first
    beam search that re-expand duplicate nodes with lower cost.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param beam_width: The size of the beam (defaults to 1).
    :type beam_width: int
    """
    closed = {}
    fringe = PrioritySet(node_value=problem.node_value,
                         max_length=beam_width)
    fringe.push(problem.initial)

    while len(fringe) > 0:
        parents = []
        while len(fringe) > 0:
            parent = fringe.pop()
            closed[parent] = parent.cost()
            if problem.goal_test(parent):
                yield parent
            parents.append(parent)

        for node in parents:
            for s in problem.successors(node):
                if s not in closed or s.cost() < closed[s]:
                    fringe.push(s)

def beam_optimization(problem, beam_width=1):
    """
    A variant of beam search that is used for optimization problems.
    """
    best = None
    best_val = float('inf')

    closed = set()
    fringe = PrioritySet(node_value=problem.node_value,
                         max_length=beam_width)
    fringe.push(problem.initial)
    closed.add(problem.initial)

    while len(fringe) > 0:
        pv = fringe.peek_value()
        if pv > best_val:
            yield best

        parents = []
        while len(fringe) > 0:
            parent = fringe.pop()
            parents.append(parent)

        best = parents[0]
        best_val = pv

        for node in parents:
            for s in problem.successors(node):
                if s not in closed:
                    fringe.push(s)
                    closed.add(s)

    yield best

def widening_beam_search(problem, initial_beam_width=1,
                               max_beam_width=1000):
    """
    A variant of beam search that successively increase the beam width when
    search fails. This ensures that if a solution exists that beam search will
    find it. However, if you are looking for multiple solutions, then it might
    return duplicates as the width is increased. 

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param initial_beam_width: The initial size of the beam (defaults to 1).
    :type initial_beam_width: int
    :param max_beam_width: The maximum size of the beam (defaults to 1000).
    :type max_beam_width: int
    """
    beam_width = initial_beam_width
    while beam_width <= max_beam_width:
        for solution in beam_search(problem, beam_width=beam_width):
            yield solution
        beam_width += 1

def depth_first_search(problem, search=graph_search):
    """
    A simple implementation of depth-first search using a LIFO queue.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param search: A search algorithm to use (defaults to graph_search).
    :type search: :func:`graph_search` or :func`tree_search`
    """
    for solution in search(problem, LIFOQueue()):
        yield solution

def breadth_first_search(problem, search=graph_search):
    """
    A simple implementation of depth-first search using a FIFO queue.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param search: A search algorithm to use (defaults to graph_search).
    :type search: :func:`graph_search` or :func`tree_search`
    """
    for solution in search(problem, FIFOQueue()):
        yield solution

def best_first_search(problem, search=graph_search, cost_limit=float('inf')):
    """
    Cost limited best-first search. By default the cost limit is set to
    `float('inf')`, so it is identical to traditional best-first search. This
    implementation uses a priority set (i.e., a sorted list without duplicates)
    to maintain the fringe.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param search: A search algorithm to use (defaults to graph_search).
    :type search: :func:`graph_search` or :func`tree_search`
    :param cost_limit: The cost limit for the search (default = `float('inf')`)
    :type cost_limit: float
    """
    for solution in search(problem, PrioritySet(node_value=problem.node_value,
                                                  cost_limit=cost_limit)):
        yield solution

def iterative_deepening_best_first_search(problem, search=graph_search,
                                          initial_cost_limit=0, cost_inc=1,
                                          max_cost_limit=float('inf')): 
    """
    A variant of iterative deepening that uses cost to determine the limit for
    expansion. When search fails, the cost limit is increased according to
    `cost_inc`. If the heuristic is admissible, then this is guranteed to find
    the best solution (similar to best first serach), but uses less memory.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param search: A search algorithm to use (defaults to graph_search).
    :type search: :func:`graph_search` or :func`tree_search`
    :param initial_cost_limit: The initial cost limit for the search.
    :type initial_cost_limit: float
    :param cost_inc: The amount to increase the cost limit after failure.
    :type cost_inc: float
    :param max_cost_limit: The maximum cost limit (default value of `float('inf')`)
    :type max_cost_limit: float
    """
    cost_limit = initial_cost_limit
    while cost_limit < max_cost_limit:
        for solution in search(problem, PrioritySet(cost_limit=cost_limit,
                                                      node_value=problem.node_value)):
            yield solution
        cost_limit += cost_inc

def hill_climbing_optimization(problem):
    """
    Steepest descent hill climbing. Probably the simplest optimization
    approach. Should yield identical results to beam_optimization when it has a
    width of 1, but doesn't need to maintain alternatives, so might use slightly
    less memory (just stores the best node instead of limited length priority
    queue). 
    """
    b = problem.initial
    bv = problem.node_value(b)
    closed=set()
    closed.add(problem.initial)

    found_better = True
    while found_better:
        found_better = False
        for s in problem.successors(b):
            if s in closed:
                continue

            closed.add(s)
            sv = problem.node_value(s)
            if sv <= bv:
                b = s
                bv = sv
                found_better = True

    yield b

def temp_exp(initial, iteration, limit):
    alpha = exp(log(0.000001 / initial) / limit)
    return initial * pow(alpha, iteration)

def temp_fast(initial, iteration, limit):
    return initial / (iteration+1)

def simulated_annealing_optimization(problem, limit=100, initial_temp=100,
                                     temp_fun=temp_exp):
    """
    A more complicated optimization technique. The best node is chosen if it is
    better than the current node. If it is not, then a node is chosen with some
    probability based on the schedule. 
    """
    b = problem.initial
    bv = problem.node_value(b)

    c = b
    cv = bv

    for t in range(limit):
        T = temp_fun(initial_temp, t, limit)
        if T == 0:
            break

        s = problem.random_successor(c)
        sv = problem.node_value(s)
        
        if sv < bv:
            b = s
            bv = sv

        delta_e = sv - cv
        if delta_e < 0 or (T > 0 and random() > 1/(1+exp(-delta_e/T))):
            c = s
            cv = sv

    yield b 

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

            try:
                sol = next(search(annotated_problem))
                value = problem.node_value(sol)
            except StopIteration:
                value = 'Failed'

            table.append([problem.__class__.__name__, search.__name__,
                          annotated_problem.goal_tests,
                          annotated_problem.nodes_expanded,
                          annotated_problem.nodes_evaluated, value])

    print(tabulate(table, headers=['Problem', 'Search Alg', 'Goal Tests',
                                   'Nodes Expanded', 'Nodes Evaluated',
                                   'Solution Cost'],
                   tablefmt="simple"))
