"""
This module contains the local search / optimization techniques. Instead of trying to
find a goal state, these algorithms try to find the lowest cost state. 
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from math import exp
from math import log
from random import random

from py_search.base import PriorityQueue

def hill_climbing(problem, random_restarts=0, graph_search=True,
                  cost_limit=float('-inf')):
    """
    Probably the simplest optimization approach. It expands the list of
    neighbors and chooses the best neighbor (steepest descent hill climbing). 
    
    Default configuration should yield similar behavior to
    :func:`local_beam_search` when it has a width of 1, but doesn't need to
    maintain alternatives, so might use slightly less memory (just stores the
    best node instead of limited length priority queue). 

    If graph_search is true (the default), then a closed list is maintained.
    This is imporant for search spaces with platues because it keeps the
    algorithm from reexpanding neighbors with the same value and getting stuck
    in a loop. 

    If random_restarts > 0, then search is restarted multiple times. This can
    be useful for getting out of local minimums. 

    Cost_limit can be used to terminate search early if a good enough solution
    has been found. 

    :param problem: The problem to solve.
    :type problem: :class:`py_search.base.Problem`
    :param random_restarts: The number of times to restart search. The
        initial state is used for the first search and subsequent starts begin
        at a random state.
    :type random_restarts: int
    :param graph_search: Whether to use graph search (no duplicates) or tree
        search (duplicates)
    :type graph_search: Boolean
    :param cost_limit: A lower bound on the cost, if a node with value <=
        cost_limit is found, then it is immediately returned. Default is -inf.
    :type cost_limit: float
    """
    b = problem.initial
    bv = problem.node_value(b)

    if bv <= cost_limit:
        yield b

    if graph_search:
        closed=set()
        closed.add(problem.initial)

    c = b
    cv = bv

    while random_restarts >= 0:
        found_better = True
        while found_better:
            found_better = False
            for s in problem.successors(c):
                if graph_search and s in closed:
                    continue
                elif graph_search:
                    closed.add(s)
                sv = problem.node_value(s)
                if sv <= bv:
                    b = s
                    bv = sv
                    if bv <= cost_limit:
                        yield b
                if sv <= cv:
                    c = s
                    cv = sv
                    found_better = True

        random_restarts -= 1
        if random_restarts >= 0:
            c = problem.random_node()
            while graph_search and c in closed:
                c = problem.random_node()
            cv = problem.node_value(c)

            if graph_search:
                closed.add(c)
            if cv <= bv:
                b = c
                bv = cv
                if bv <= cost_limit:
                    yield b

    yield b

def local_beam_search(problem, beam_width=1, graph_search=True,
                      cost_limit=float('-inf')):
    """
    A variant of :func:`py_search.informed_search.beam_search` that can be
    applied to local search problems.  When the beam width of 1 this approach
    yields behavior similar to :func:`hill_climbing`.

    :param problem: The problem to solve.
    :type problem: :class:`py_search.base.Problem`
    :param beam_width: The size of the search beam.
    :type beam_width: int
    :param graph_search: Whether to use graph search (no duplicates) or tree
        search (duplicates)
    :type graph_search: Boolean
    """
    b = None
    bv = float('inf')

    fringe = PriorityQueue(node_value=problem.node_value)
    fringe.push(problem.initial)

    while len(fringe) < beam_width:
        fringe.push(problem.random_node())
    
    if graph_search:
        closed = set()
        closed.add(problem.initial)

    while len(fringe) > 0:
        pv = fringe.peek_value()

        if pv > bv:
            yield b

        parents = []
        while len(fringe) > 0 and len(parents) < beam_width:
            parent = fringe.pop()
            parents.append(parent)
        fringe.clear()

        b = parents[0]
        bv = pv

        for node in parents:
            for s in problem.successors(node):
                added = True
                if not graph_search:
                    fringe.push(s)
                elif s not in closed:
                    fringe.push(s)
                    closed.add(s)
                else:
                    added = False

                if added and fringe.peek_value() <= cost_limit:
                    yield fringe.peek()


    yield b

def simulated_annealing(problem, temp_factor=0.95, temp_length=None,
                        initial_temp=None, init_prob=0.4, min_accept=0.02,
                        cost_limit=float('-inf'), limit=float('inf')):
    """
    A more complicated optimization technique. At each iteration a random
    successor is expanded if it is better than the current node. If the random
    successor is not better than the current node, then it is expanded with some
    probability based on the temperature.

    Used the formulation of simulated annealing found in:
        Johnson, D. S., Aragon, C. R., McGeoch, L. A., & Schevon, C. (1989).
        Optimization by simulated annealing: an experimental evaluation; part
        I, graph partitioning. Operations research, 37(6), 865-892.

    :param problem: The problem to solve.
    :type problem: :class:`py_search.base.Problem`
    :param temp_factor: The factor for geometric cooling, a value between 0 and
        1, but usually very close to 1. 
    :type temp_factor: float
    :param temp_length: The number of nodes to expand at each temperature. If
        set to `None` (the default) then it is automatically chosen to be equal
        to the length of the successors list.
    :type temp_length: int
    :param initial_temp: The initial temperature for the annealing. The number
        is objective function specific. If set to None (the default), then
        a semi-random walk is used to select an initial
        temperature that will yield approx. init_prob acceptance rate for
        worse states.
    :type initial_temp: float or None
    :param min_accept: The fraction of states that must be accepted in
        temp_length iterations (taken from a single temperature) to not be
        frozen.  Every time this is not exceeded, the frozen counter is
        incremented until it hits 5. If a better state is found, then the
        frozen counter is reset to 0.
    :type min_accept: float between 0 and 1
    :param cost_limit: A lower bound on the cost, if a node with value <=
        cost_limit is found, then it is immediately returned. Default is -inf.
    :type cost_limit: float
    :param limit: The maximum number of iterations (random neighbors) to expand
        before stopping. 
    :type limit: float
    """
    T = initial_temp
    b = problem.initial
    bv = problem.node_value(b)

    if bv <= cost_limit:
        yield b

    c = b
    cv = bv

    frozen = 0
    iterations = 0

    if temp_length is None:
        temp_length = len(list(problem.successors(c)))
        print("Temp length set equal to number of initial neighbors (%i)" %
              temp_length)

    if T is None:
        delta_sum = 0
        delta_count = 0

    while frozen < 5:
        acceptances = 0

        for i in range(temp_length):
            iterations += 1
            s = problem.random_successor(c)
            sv = problem.node_value(s)

            if sv < bv:
                b = s
                bv = sv
                frozen = 0

            if bv <= cost_limit or iterations >= limit:
                yield b

            delta_e = sv - cv
            if T is None and delta_e > 0:
                delta_sum += delta_e
                delta_count += 1
            if (delta_e <= 0 or (T is None and random() < 0.5) or 
                (T is not None and T > 1e-2 and random() < exp(-delta_e/T))):
                acceptances += 1
                c = s
                cv = sv

        if T is None:
            if delta_count > 100:
                avg_delta = delta_sum / delta_count
                T = -avg_delta / log(init_prob)
                print("Initial temperature set to: %0.3f (based on %i samples)" %
                      (T, delta_count))
        else:
            T = temp_factor * T

        if (acceptances / temp_length) < min_accept:
            frozen += 1

    yield b
