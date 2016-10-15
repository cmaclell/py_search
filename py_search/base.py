""" 
This module contains the data_structures used in py_search. In
particular, it contains the the :class:`Problem` class, which is used to represent
the different search problems, and the :class:`AnnotatedProblem` class, which wraps 
around a specific problem and keeps track of the number of core method
calls. 

At a lower level this module also contains the :class:`Node` class, which is used
to represent a node in the search space. 

Finally, the module contains the :class:`Fringe` class, and its instantiations
(:class:`FIFOQueue`, :class:`LIFOQueue`, and :class:`PrioritySet`). A Fringe is
used to structure the way a search space is explored.
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from collections import deque
from blist import sortedlist

class Problem(object):
    """
    The basic problem to solve. The main functions that must be defined include
    successors and goal_test. Some search techniques also require the
    random_successor and predecessors methods to be implemented.
    """
    def __init__(self, initial, parent=None, action=None, initial_cost=0,
                 extra=None):
        self.initial = Node(initial, parent, action, initial_cost, extra=extra)

    def node_value(self, node):
        """
        Returns the the value of the current node. This is the value being
        minimized by the search. By default the path_cost is used, but this
        function can be overloaded to include a heuristic.
        """
        return node.cost()

    def successors(self, node):
        """
        An iterator that yields all of the successors of the current node.
        """
        raise NotImplemented("No successors function implemented")

    def random_successor(self, node):
        """
        This method should return a single successor node. This is used
        by some of the local search / optimization techniques. 
        """
        raise NotImplemented("No random successor implemented!")

    def random_node(self):
        """
        This method returns a random node in the search space. This 
        is used by some of the local search / optimization techniques.
        """
        raise NotImplemented("No random node implemented!")

    def goal_test(self, node):
        """
        Returns true if a goal state is found. This is typically used not used
        by the local search / optimization techniques.
        """
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

    def random_successor(self, node):
        """
        A wrapper for the random_successor method that keeps track of the
        number of nodes expanded.
        """
        self.nodes_expanded += 1
        return self.problem.random_successor(node)

    def random_node(self):
        """
        A wrapper for the random_node method.
        """
        return self.problem.random_node()

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
    :param extra: extra information to store in this node, typically used to
                  store non-hashable information about the state.
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
        (no tail recursion in python).
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
    >>> fifo.push(0)
    >>> fifo.push(1)
    >>> fifo.push(2)
    >>> print(fifo.pop())
    0
    >>> print(fifo.pop())
    1
    >>> print(fifo.pop())
    2
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
    >>> lifo.push(0)
    >>> lifo.push(1)
    >>> lifo.push(2)
    >>> print(lifo.pop())
    2
    >>> print(lifo.pop())
    1
    >>> print(lifo.pop())
    0
    """

    def pop(self):
        return self.nodes.pop()

class PriorityQueue(Fringe):
    """ 
    A priority set that sorts elements by their value. Always returns the
    minimum value item. When a duplicate node is added the one with the minimum
    value is kept. A :class:`PrioritySet` accepts a node_value function, a
    cost_limit (nodes with a value greater than this limit will not be added)
    and a max_length parameter. If adding an item ever causes the size to
    exceed the max_length then the worst nodes are removed until the list is
    equal to max_length.

    >>> pq = PriorityQueue(node_value=lambda x: x, max_length=3)
    >>> pq.push(6)
    >>> pq.push(0)
    >>> pq.push(2)
    >>> pq.push(6)
    >>> pq.push(7)
    >>> print(len(pq))
    3
    >>> print(pq.pop())
    0
    >>> print(pq.pop())
    2
    >>> print(pq.pop())
    6

    :param node_value: The node evaluation function (defaults to 
        ``lambda x: x.cost()``)
    :type node_value: a function with one parameter for node
    :param cost_limit: the maximum value for elements in the set, if an item
        exceeds this limit then it will not be added (defaults to
        ``float('inf'))``
    :type cost_limit: float
    :param max_length: The maximum length of the list (defaults to
        ``float('inf')``
    :type max_length: int or ``float('inf')``
    """
    def __init__(self, node_value=lambda x: x.cost(), cost_limit=float('inf'),
                 max_length=float('inf')):
        self.nodes = sortedlist()
        self.max_length = max_length
        self.cost_limit = cost_limit
        self.node_value = node_value

    def clear(self):
        """
        Empties the sorted list.
        """
        self.nodes = sortedlist()

    def peek(self):
        """
        Returns the best node.
        """
        return self.nodes[0][1]

    def peek_value(self):
        """
        Returns the value of the best node.
        """
        return self.nodes[0][0]

    def push(self, node):
        """
        Push a node into the priority queue. If the node exceeds the cost limit
        then it is not added. If the max_length is exceeded by
        adding the node, then the worst node is discarded from the set. 
        """
        value = self.node_value(node)

        if value > self.cost_limit:
            return

        self.nodes.add((value, node))

        if len(self.nodes) > self.max_length:
            val, node = self.nodes.pop()

    def pop(self):
        """
        Pop the best value from the priority queue.
        """
        val, node = self.nodes.pop(0)
        return node

    def __len__(self):
        return len(self.nodes)

