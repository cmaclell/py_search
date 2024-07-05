"""
This module includes the informed search techniques: :func:`best_first_search`
(i.e., A*), :func:`iterative_deepening_best_first_search` (i.e., IDA*),
:func:`beam_search`, and :func:`widening_beam_search`.
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division
import threading

from functools import partial

from py_search.base import SolutionNode
from py_search.base import PriorityQueue
from py_search.base import NbsDataStructure
from py_search.uninformed import choose_search


def best_first_search(problem, cost_limit=float('inf'), graph=True,
                      forward=True, backward=False):
    """
    Cost limited best-first search. By default the cost limit is set to
    `float('inf')`, so it is identical to traditional best-first search. This
    implementation uses a priority queue to maintain the fringe.

    If the problem.node_value is the cost to reach the node plus an admissible
    heuristic estimate of the distance from the node to the goal, then this is
    the A* algorithm.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param search: A search algorithm to use (defaults to graph_search).
    :type search: :func:`graph_search` or :func`tree_search`
    :param cost_limit: The cost limit for the search (default = `float('inf')`)
    :type cost_limit: float
    """
    for solution in choose_search(problem,
                                  partial(PriorityQueue,
                                          node_value=problem.node_value,
                                          cost_limit=cost_limit),
                                  graph=graph, forward=forward,
                                  backward=backward):
        yield solution


def iterative_deepening_best_first_search(problem, initial_cost_limit=0,
                                          cost_inc=1,
                                          max_cost_limit=float('inf'),
                                          graph=True, forward=True,
                                          backward=False):
    """
    A variant of iterative deepening that uses cost to determine the limit for
    expansion. When search fails, the cost limit is increased according to
    `cost_inc`. If the heuristic is admissible, then this is guranteed to find
    the best solution (similar to best first serach), but uses less memory.

    If the problem.node_value is the cost to reach the node plus an admissible
    heuristic estimate of the distance from the node to the goal, then this is
    the IDA* algorithm.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param search: A search algorithm to use (defaults to graph_search).
    :type search: :func:`graph_search` or :func`tree_search`
    :param initial_cost_limit: The initial cost limit for the search.
    :type initial_cost_limit: float
    :param cost_inc: The amount to increase the cost limit after failure.
    :type cost_inc: float
    :param max_cost_limit: The maximum cost limit (default value of
        `float('inf')`)
    :type max_cost_limit: float
    """
    cost_limit = initial_cost_limit
    while cost_limit < max_cost_limit:
        for solution in choose_search(problem,
                                      partial(PriorityQueue,
                                              node_value=problem.node_value,
                                              cost_limit=cost_limit),
                                      graph=graph, forward=forward,
                                      backward=backward):
            yield solution
        cost_limit += cost_inc


def beam_search(problem, beam_width=1, graph=True):
    """
    A variant of breadth-first search where all nodes in the fringe
    are expanded, but the resulting new fringe is limited to have length
    beam_width, where the nodes with the worst value are dropped. The default
    beam width is 1, which yields greedy best-first search (i.e., hill
    climbing).

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
    :param graph_search: whether to use graph or tree search.
    :type graph_search: boolean
    """
    closed = {}
    fringe = PriorityQueue(node_value=problem.node_value)
    fringe.push(problem.initial)
    closed[problem.initial] = problem.initial.cost()

    while len(fringe) > 0:
        parents = []
        while len(fringe) > 0 and len(parents) < beam_width:
            parent = fringe.pop()
            if problem.goal_test(parent, problem.goal):
                yield SolutionNode(parent, problem.goal)
            parents.append(parent)
        fringe.clear()

        for node in parents:
            for s in problem.successors(node):
                if not graph:
                    fringe.push(s)
                elif s not in closed or s.cost() < closed[s]:
                    fringe.push(s)
                    closed[s] = s.cost()


def widening_beam_search(problem, initial_beam_width=1,
                         max_beam_width=1000, graph=True):
    """
    A variant of beam search that successively increase the beam width when
    search fails. This ensures that if a solution exists, and you're using
    graph search, and the solution space is finite, then that beam search will
    find it.

    However, if you are looking for multiple solutions, then it might return
    duplicates as the width is increased. As the beam width increase, behavior
    is closer and closer to breadth-first search.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    :param initial_beam_width: The initial size of the beam (defaults to 1).
    :type initial_beam_width: int
    :param max_beam_width: The maximum size of the beam (defaults to 1000).
    :type max_beam_width: int
    """
    beam_width = initial_beam_width
    while beam_width <= max_beam_width:
        for solution in beam_search(problem, beam_width=beam_width,
                                    graph=graph):
            yield solution
        beam_width += 1


def near_optimal_front_to_end_bidirectional_search(problem):
    """
    Performs a near-optimal bidirectional search (NBS) from front to end, using a
    heuristic node value to guide the search. Returns an iterator to the
    solutions, allowing for multiple solutions to be found.

    :param problem: The problem to solve.
    :type problem: :class:`Problem`
    """
    c = float("inf")
    current_solution = None
    F = problem.node_value
    fringe = NbsDataStructure(node_value_waiting=F, node_value_ready=lambda n: n.cost())

    fclosed = {}
    bclosed = {}

    fringe.push_front(problem.initial)
    fclosed[problem.initial] = problem.initial.cost()

    fringe.push_back(problem.goal)
    bclosed[problem.goal] = problem.goal.cost()

    while len(fringe) > 0:
        succeed = fringe.prepare_best()
        if not succeed:
            raise ValueError("Failed to prepare next node pair")

        u_min, v_min = fringe.peek_ready_pair()
        lower_bound = max(F(u_min), F(v_min), u_min.cost() + v_min.cost())

        if lower_bound >= c:
            yield current_solution

        # Forward Expand
        u_min = fringe.pop_front()
        for s in problem.successors(u_min):
            for goal in fringe.back():
                if problem.goal_test(u_min, goal):
                    if c > u_min.cost() + goal.cost():
                        c = u_min.cost() + goal.cost()
                        current_solution = SolutionNode(u_min, goal)
            if s not in fclosed or s.cost() < fclosed[s]:
                fringe.push_front(s)
                fclosed[s] = s.cost()

        # Backward Expand
        v_min = fringe.pop_back()
        for p in problem.predecessors(v_min):
            for state in fringe.front():
                if problem.goal_test(state, v_min):
                    if c > v_min.cost() + state.cost():
                        c = v_min.cost() + state.cost()
                        current_solution = SolutionNode(state, v_min)
            if p not in bclosed or p.cost() < bclosed[p]:
                fringe.push_back(p)
                bclosed[p] = p.cost()

    yield current_solution
