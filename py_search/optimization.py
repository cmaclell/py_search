"""
This module contains the local search / optimization techniques. Instead of trying to
find a goal state, these algorithms try to find the lowest cost state. 
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from math import exp
from math import pow
from math import log
from random import random

from py_search.base import PriorityQueue

def hill_climbing(problem, random_restarts=0, graph_search=True):
    """
    Steepest descent hill climbing. Probably the simplest optimization
    approach. Should yield identical results to :func:`local_beam_search` when
    it has a width of 1, but doesn't need to maintain alternatives, so might
    use slightly less memory (just stores the best node instead of limited
    length priority queue). 

    :param problem: The problem to solve.
    :type problem: :class:`py_search.base.Problem`
    :param random_restarts: The number of times to restart search. The
        initial state is used for the first search and subsequent starts begin
        at a random state.
    :type random_restarts: int
    :param graph_search: Whether to use graph search (no duplicates) or tree
        search (duplicates)
    :type graph_search: Boolean
    """
    b = problem.initial
    bv = problem.node_value(b)

    if graph_search:
        closed=set()
        closed.add(problem.initial)

    c = b
    cv = bv

    while random_restarts >= 0:
        found_better = True
        while found_better:
            found_better = False
            for s in problem.successors(b):
                if graph_search and s in closed:
                    continue
                elif graph_search:
                    closed.add(s)
                sv = problem.node_value(s)
                if sv <= bv:
                    b = s
                    bv = sv
                if sv <= cv:
                    b = s
                    cv = sv
                    found_better = True

        random_restarts -= 1
        if random_restarts >= 0:
            c = problem.random_node()
            cv = problem.node_value(c)
            if graph_search:
                closed.add(problem.initial)
            if cv <= bv:
                b = c
                bv = cv

    yield b

def local_beam_search(problem, beam_width=1, graph_search=True):
    """
    A variant of :func:`py_search.informed_search.beam_search` that can be
    applied to local search problems.  When the beam width of 1 this approach
    yields identical behavior to :func:`hill_climbing`.

    :param problem: The problem to solve.
    :type problem: :class:`py_search.base.Problem`
    :param beam_width: The size of the search beam.
    :type beam_width: int
    :param graph_search: Whether to use graph search (no duplicates) or tree
        search (duplicates)
    :type graph_search: Boolean
    """
    best = None
    best_val = float('inf')

    fringe = PriorityQueue(node_value=problem.node_value)
    fringe.push(problem.initial)

    while len(fringe) < beam_width:
        fringe.push(problem.random_node())
    
    if graph_search:
        closed = set()
        closed.add(problem.initial)

    while len(fringe) > 0:
        pv = fringe.peek_value()
        if pv > best_val:
            yield best

        parents = []
        while len(fringe) > 0 and len(parents) < beam_width:
            parent = fringe.pop()
            parents.append(parent)
        fringe.clear()

        best = parents[0]
        best_val = pv

        for node in parents:
            for s in problem.successors(node):
                if not graph_search:
                    fringe.push(s)
                elif s not in closed:
                    fringe.push(s)
                    closed.add(s)

    yield best

def temp_exp(initial, iteration, limit):
    """
    An exponential (alpha^x) cooling schedule. The exponential cooling rate is
    selected so that the function reaches a temperature of 0.000001 at the
    limit. 
    """
    alpha = exp(log(0.000001 / initial) / limit)
    return initial * pow(alpha, iteration)

def temp_fast(initial, iteration, limit):
    """
    A fast (1/x) cooling strategy. 
    """
    return initial / (iteration+1)

def simulated_annealing(problem, limit=100, initial_temp=100,
                        exponential_cooling=True):
    """
    A more complicated optimization technique. At each iteration a random
    successor is expanded if it is better than the current node. If the random
    successor is not better than the current node, then it is expanded with some
    probability based on the temperature.

    :param problem: The problem to solve.
    :type problem: :class:`py_search.base.Problem`
    :param limit: The maximum number of nodes to evaluate.
    :type limit: int
    :param initial_temp: The initial temperature (default is 100).
    :type initial_temp: int
    :param exponential_cooling: Whether to use exponential
        (initial_temp*alph^k) or fast (initial_temp / k) cooling.
    :type exponential_cooling: boolean
    """
    if exponential_cooling:
        temp_fun = temp_exp
    else:
        tem_fun = temp_fast

    b = problem.initial
    bv = problem.node_value(b)

    c = b
    cv = bv

    for t in range(limit):
        T = temp_fun(initial_temp, t, limit)
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
