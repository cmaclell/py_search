"""
This module includes the core search methods :func:`tree_search` and
`graph_search` and the primary uninformed search techniques:
:func:`depth_first_search`, :func:`breadth_first_search`, and
:func:`iterative_deepening_search`.
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from py_search.base import LIFOQueue
from py_search.base import FIFOQueue


def tree_search(problem, fringe, depth_limit=float('inf')):
    """
    Perform tree search (i.e., search where states might be duplicated) using
    the given fringe class.Returns an iterators to the solutions, so more than
    one solution can be found.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param fringe: The fringe class to use.
    :type fringe: :class:`fringe`
    :param depth_limit: A limit for the depth of the search tree. If set to
        float('inf'), then depth is unlimited.
    :type depth_limit: int or float('inf')
    """
    fringe.push(problem.initial)

    while len(fringe) > 0:
        node = fringe.pop()

        if problem.goal_test(node):
            yield node
        elif depth_limit == float('inf') or node.depth() < depth_limit:
            fringe.extend(problem.successors(node))


def graph_search(problem, fringe, depth_limit=float('inf')):
    """
    Perform graph search (i.e., no duplicate states) using the given fringe
    class. Returns an iterator to the solutions, so more than one solution can
    be found.

    Note that the closed list will allow re-expansion of nodes with a lower
    cost.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param fringe: The fringe class to use.
    :type fringe: :class:`fringe`
    :param depth_limit: A limit for the depth of the search tree. If set to
        float('inf'), then depth is unlimited.
    :type depth_limit: int or float('inf')
    """
    closed = {}
    fringe.push(problem.initial)
    closed[problem.initial] = problem.initial.cost()

    while len(fringe) > 0:
        node = fringe.pop()
        if problem.goal_test(node):
            yield node
        elif depth_limit == float('inf') or node.depth() < depth_limit:
            for s in problem.successors(node):
                if s not in closed or s.cost() < closed[s]:
                    fringe.push(s)
                    closed[s] = s.cost()


def depth_first_search(problem, depth_limit=float('inf'), search=graph_search):
    """
    A simple implementation of depth-first search using a LIFO queue.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param search: A search algorithm to use (defaults to graph_search).
    :type search: :func:`graph_search` or :func`tree_search`
    :param depth_limit: A limit for the depth of the search tree. If set to
        float('inf'), then depth is unlimited.
    :type depth_limit: int or float('inf')
    """
    for solution in search(problem, LIFOQueue(), depth_limit):
        yield solution


def breadth_first_search(problem, depth_limit=float('inf'),
                         search=graph_search):
    """
    A simple implementation of depth-first search using a FIFO queue.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param search: A search algorithm to use (defaults to graph_search).
    :type search: :func:`graph_search` or :func`tree_search`
    :param depth_limit: A limit for the depth of the search tree. If set to
        float('inf'), then depth is unlimited.
    :type depth_limit: int or float('inf')
    """
    for solution in search(problem, FIFOQueue(), depth_limit):
        yield solution


def iterative_deepening_search(problem, search=graph_search,
                               initial_depth_limit=0, depth_inc=1,
                               max_depth_limit=float('inf')):
    """
    An implementation of iterative deepening search. This search is basically
    depth-limited depth first up to the depth limit. If no solution is found at
    the current depth limit then the depth limit is increased by depth_inc and
    the depth-limited depth first search is restarted.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param search: A search algorithm to use (defaults to graph_search).
    :type search: :func:`graph_search` or :func`tree_search`
    :param initial_depth_limit: The initial depth limit for the search.
    :type initial_depth_limit: int or float('inf')
    :param depth_inc: The amount to increase the depth limit after failure.
    :type depth_inc: int
    :param max_depth_limit: The maximum depth limit (default value of
        `float('inf')`)
    :type max_depth_limit: int or float('inf')
    """
    depth_limit = initial_depth_limit
    while depth_limit < max_depth_limit:
        for solution in depth_first_search(problem, depth_limit, search):
            yield solution
        depth_limit += depth_inc
