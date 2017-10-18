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
from py_search.base import Node


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


def iterative_sampling(problem, num_samples=float('inf'),
                       depth_limit=float('inf')):
    """
    A non-systematic alternative to depth-first search. This samples paths
    through the tree until a dead end or until the depth limit is reached. It
    has much lower memory requirements than depth-first or breadth-first
    search, but requires the user to specify num_samples and depth_limit
    parameters. The search will return non-optimal paths (it does not evaluate
    node values) and sometimes it may fail to find solutions if the number of
    samples or depth limit is too low.

    A full description of the algorithm and the mathematics that support it can
    be found here:

        Langley, P. (1992, May). Systematic and nonsystematic search
        strategies. In Artificial Intelligence Planning Systems: Proceedings of
        the First International Conference (pp. 145-152).

    This technique is included with the other uninformed methods because it is
    uninformed when random_successor uniform randomly generates successors.
    However, this technique could be converted into an informed technique if
    random_successor is implemented with an approach that samples successors
    according to their node_value.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param search: A search algorithm to use (defaults to graph_search).
    :type search: :func:`graph_search` or :func`tree_search`
    :param num_samples: The number of samples through the search tree. If no
        solution is found after collecting this many samples, then the search
        fails.
    :type num_samples: int or float('inf') (default of float('inf'))
    :param max_depth_limit: The maximum depth limit (default value of
        `float('inf')`)
    :type max_depth_limit: int or float('inf') (default of float('inf'))
    """
    for i in range(num_samples):
        curr = problem.initial
        while curr:
            if problem.goal_test(curr):
                yield curr
            elif depth_limit == float('inf') or curr.depth() < depth_limit:
                curr = problem.random_successor(curr)
            else:
                curr = False


def bidirectional_graph_search(problem, depth_limit=float('inf')):
    """
    A uninformed technique that searchs simultaneously in both the forward and
    backward directions.
    """
    forward_fringe = FIFOQueue()
    forward_closed = {}
    forward_fringe.push(problem.initial)
    forward_closed[problem.initial] = problem.initial.cost()

    backward_fringe = FIFOQueue()
    backward_closed = {}
    backward_fringe.push(problem.goal)
    backward_closed[problem.goal] = problem.goal.cost()

    while len(forward_fringe) > 0 and len(backward_fringe) > 0:
        node = forward_fringe.pop()
        for g in backward_fringe.nodes:
            if problem.state_goal_test(node, g):
                curr_g = g
                while curr_g is not None:
                    if curr_g.parent is None:
                        p_cost = 0
                    else:
                        p_cost = curr_g.parent.cost()
                    node = Node(g, node, curr_g.action, node.cost() +
                                curr_g.cost() - p_cost)
                    curr_g = curr_g.parent
                yield node
        else:
            if depth_limit == float('inf') or node.depth() < depth_limit:
                for s in problem.successors(node):
                    if s not in forward_closed or s.cost() < forward_closed[s]:
                        forward_fringe.push(s)
                        forward_closed[s] = s.cost()

        node = backward_fringe.pop()
        for s in forward_fringe.nodes:
            if problem.state_goal_test(s, node):
                curr_g = node
                node = s
                while curr_g is not None:
                    if curr_g.parent is None:
                        p_cost = 0
                    else:
                        p_cost = curr_g.parent.cost()
                    node = Node(g, node, curr_g.action, node.cost() +
                                curr_g.cost() - p_cost)
                    curr_g = curr_g.parent
                yield node
        else:
            if depth_limit == float('inf') or node.depth() < depth_limit:
                for s in problem.predecessors(node):
                    if (s not in backward_closed or s.cost() < backward_closed[s]):
                        backward_fringe.push(s)
                        backward_closed[s] = s.cost()
