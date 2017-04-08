"""
Tests for the optimization search techniques.
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from random import normalvariate

from py_search.base import Node
from py_search.base import Problem
from py_search.base import AnnotatedProblem
from py_search.optimization import hill_climbing
from py_search.optimization import local_beam_search
from py_search.optimization import simulated_annealing
from py_search.optimization import branch_and_bound
from py_search.utils import compare_searches


class PlateauProblem(Problem):

    def successors(self, node):
        for i in range(100):
            v = node.state + normalvariate(0, 1)
            yield Node(v, node, 'expand', max(min(v, node.extra[1]),
                       node.extra[0]), extra=node.extra)

    def random_successor(self, node):
        v = node.state + normalvariate(0, 1)
        return Node(v, node, 'expand', max(min(v, node.extra[1]),
                                           node.extra[0]), extra=node.extra)

    def goal_test(self, node):
        return False


class EasyProblem(Problem):

    def successors(self, node):
        for i in range(100):
            v = node.cost() + normalvariate(0, 1)
            if v < node.extra[1] and v > node.extra[0]:
                yield Node(v, node, 'expand', v, extra=node.extra)

    def random_successor(self, node):
        v = -11
        while v <= node.extra[0] or v >= node.extra[1]:
            v = node.cost() + normalvariate(0, 1)
        return Node(v, node, 'expand', v, extra=node.extra)

    def goal_test(self, node):
        return False


def test_hill_climbing():
    initial = 0
    goal = 10
    limits = (-goal, goal)
    p = AnnotatedProblem(EasyProblem(initial, initial_cost=initial,
                                     extra=limits))
    sol = next(hill_climbing(p, graph_search=False))
    assert abs(sol.state - limits[0]) <= 0.1


def test_local_beam_search():
    initial = 0
    goal = 10
    limits = (-goal, goal)
    p = AnnotatedProblem(EasyProblem(initial, initial_cost=initial,
                                     extra=limits))
    sol = next(local_beam_search(p, graph_search=False))
    assert abs(sol.state - limits[0]) <= 0.1


def test_simulated_annealing():
    initial = 0
    goal = 10
    limits = (-goal, goal)
    p = AnnotatedProblem(EasyProblem(initial, initial_cost=initial,
                                     extra=limits))
    sol = next(simulated_annealing(p))
    assert abs(sol.state - limits[0]) <= 0.1


def test_branch_and_bound():
    initial = 0
    goal = 10
    limits = (-goal, goal)
    p = AnnotatedProblem(EasyProblem(initial, initial_cost=initial,
                                     extra=limits))
    sol = next(branch_and_bound(p))
    assert abs(sol.state - limits[0]) <= 0.1
