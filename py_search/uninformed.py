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
from py_search.base import JoinNode


def tree_search(problem, fringe, depth_limit=float('inf')):
    """
    Perform tree search (i.e., search where states might be duplicated) using
    the given fringe class. Returns an iterators to the solutions, so more than
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

        if problem.goal_test(node, problem.goal):
            yield node
        elif depth_limit == float('inf') or node.depth() < depth_limit:
            fringe.extend(problem.successors(node))


def bidirectional_tree_search(problem, forward_fringe=None,
                              backward_fringe=None, depth_limit=float('inf')):
    """
    A generalization of tree search that supports search in either, or both,
    directions using the provided fringe classes. Returns an iterator to the
    solutions, so more than one solution can be found.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param ffringe: The fringe class to use in the forward direction.
    :type ffringe: :class:`fringe`
    :param bfringe: The fringe class to use in the reverse direction.
    :type ffringe: :class:`fringe`
    :param depth_limit: A limit for the depth of the search tree from either
        direction. If set to float('inf'), then depth is unlimited.
    :type depth_limit: int or float('inf')
    """
    if (forward_fringe is None and backward_fringe is None):
        raise Exception("Must provide a fringe class for forward, backward"
                        "or both.")

    if forward_fringe is None:
        ffringe = [problem.initial]
    else:
        ffringe = forward_fringe
        ffringe.push(problem.initial)

    if backward_fringe is None:
        bfringe = [problem.goal]
    else:
        bfringe = backward_fringe
        bfringe.push(problem.goal)

    while len(ffringe) > 0 and len(bfringe) > 0:

        if forward_fringe is not None:
            state = ffringe.pop()
            for goal in bfringe:
                if problem.goal_test(state, goal):
                    yield state
            else:
                if depth_limit == float('inf') or state.depth() < depth_limit:
                    ffringe.extend(problem.successors(state))

        if backward_fringe is not None:
            goal = bfringe.pop()
            for state in ffringe:
                if problem.goal_test(state, goal):
                    yield state
            else:
                if depth_limit == float('inf') or goal.depth() < depth_limit:
                    bfringe.extend(problem.predecessors(goal))


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
        if problem.goal_test(node, problem.goal):
            yield node
        elif depth_limit == float('inf') or node.depth() < depth_limit:
            for s in problem.successors(node):
                if s not in closed or s.cost() < closed[s]:
                    fringe.push(s)
                    closed[s] = s.cost()


def bidirectional_graph_search(problem, forward_fringe=None,
                               backward_fringe=None, depth_limit=float('inf')):
    """
    A uninformed technique that searchs simultaneously in both the forward and
    backward directions.
    """
    if (forward_fringe is None and backward_fringe is None):
        raise Exception("Must provide a fringe class for forward, backward"
                        "or both.")

    if forward_fringe is None:
        ffringe = [problem.initial]
    else:
        ffringe = forward_fringe
        fclosed = {}
        ffringe.push(problem.initial)
        fclosed[problem.initial] = problem.initial.cost()

    if backward_fringe is None:
        bfringe = [problem.goal]
    else:
        bfringe = backward_fringe
        bclosed = {}
        bfringe.push(problem.goal)
        bclosed[problem.goal] = problem.goal.cost()

    while len(ffringe) > 0 and len(bfringe) > 0:

        if forward_fringe is not None:
            state = ffringe.pop()
            for goal in bfringe:
                if problem.goal_test(state, goal):
                    yield JoinNode(state, goal)
            else:
                if depth_limit == float('inf') or state.depth() < depth_limit:
                    for s in problem.successors(state):
                        if s not in fclosed or s.cost() < fclosed[s]:
                            ffringe.push(s)
                            fclosed[s] = s.cost()

        if backward_fringe is not None:
            goal = bfringe.pop()
            for state in ffringe:
                if problem.goal_test(state, goal):
                    yield JoinNode(state, goal)

            else:
                if depth_limit == float('inf') or goal.depth() < depth_limit:
                    for p in problem.predecessors(goal):
                        if (p not in bclosed or p.cost() < bclosed[p]):
                            bfringe.push(p)
                            bclosed[p] = p.cost()


def choose_search(problem, queue_class, depth_limit=float('inf'),
                  search="graph", direction="forward"):
    """
    Given the arguments, chooses the appropriate underlying classes
    to instantiate the search.
    """
    if direction == "forward" and search == "tree":
        return tree_search(problem, queue_class(), depth_limit)
    elif direction == "forward" and search == "graph":
        return graph_search(problem, queue_class(), depth_limit)
    if direction == "backward":
        forward_fringe = None
        backward_fringe = queue_class()
    elif direction == "both":
        forward_fringe = queue_class()
        backward_fringe = queue_class()
    else:
        raise Exception("Direction must be forward, backward, or both.")

    if search == "tree":
        search = bidirectional_tree_search
    elif search == "graph":
        search = bidirectional_graph_search
    else:
        raise Exception("Search must be tree or graph.")

    return search(problem, forward_fringe=forward_fringe,
                  backward_fringe=backward_fringe, depth_limit=depth_limit)


def depth_first_search(problem, depth_limit=float('inf'), search="graph",
                       direction="forward"):
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
    for solution in choose_search(problem, LIFOQueue, depth_limit=depth_limit,
                                  search=search, direction=direction):
        yield solution

    # for solution in search(problem, LIFOQueue(), depth_limit):
    #     yield solution


def breadth_first_search(problem, depth_limit=float('inf'),
                         search="graph", direction="forward"):
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
    for solution in choose_search(problem, FIFOQueue, depth_limit=depth_limit,
                                  search=search, direction=direction):
        yield solution
    # for solution in search(problem, FIFOQueue(), depth_limit):
    #     yield solution


def iterative_deepening_search(problem, search="graph",
                               initial_depth_limit=0, depth_inc=1,
                               max_depth_limit=float('inf'),
                               direction="forward"):
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
        for solution in depth_first_search(problem, depth_limit=depth_limit,
                                           search=search, direction=direction):
            yield solution
        depth_limit += depth_inc


def iterative_sampling(problem, max_samples=float('inf'),
                       depth_limit=float('inf')):
    """
    A non-systematic alternative to depth-first search. This samples paths
    through the tree until a dead end or until the depth limit is reached. It
    has much lower memory requirements than depth-first or breadth-first
    search, but requires the user to specify max_samples and depth_limit
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
    :param max_samples: The maximum number of samples through the search tree.
        If no solution is found after collecting this many samples, then the
        search fails.
    :type max_samples: int or float('inf') (default of float('inf'))
    :param max_depth_limit: The maximum depth limit (default value of
        `float('inf')`)
    :type max_depth_limit: int or float('inf') (default of float('inf'))
    """
    num_samples = 0
    while num_samples < max_samples:
        curr = problem.initial
        while curr:
            if problem.goal_test(curr, problem.goal):
                yield curr
            elif depth_limit == float('inf') or curr.depth() < depth_limit:
                curr = problem.random_successor(curr)
            else:
                curr = False
