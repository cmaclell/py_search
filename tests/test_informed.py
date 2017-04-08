"""
Tests for the informed search techniques.
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from math import pow

from py_search.base import Node
from py_search.base import Problem
from py_search.base import AnnotatedProblem
from py_search.uninformed import tree_search
from py_search.uninformed import graph_search
from py_search.informed import best_first_search
from py_search.informed import iterative_deepening_best_first_search
from py_search.informed import beam_search


class EasyProblem(Problem):

    def successors(self, node):
        yield Node(node.state+1, node, 'expand', node.cost() + 1,
                   extra=node.extra)
        yield Node(node.state+1, node, 'expand', node.cost() + 1,
                   extra=node.extra)

    def goal_test(self, node):
        return node.state == node.extra


class HeuristicEasyProblem(Problem):

    def node_value(self, node):
        return (node.extra - node.state)

    def successors(self, node):
        yield Node(node.state + 1, node, 'expand', node.cost() + 1,
                   extra=node.extra)
        yield Node(node.state + 1, node, 'expand', node.cost() + 1,
                   extra=node.extra)

    def goal_test(self, node):
        return node.state == node.extra


def test_best_first_search_without_heuristic():
    """
    Best first search without a heuristic is essentially breadth first.
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(EasyProblem(0, extra=goal))
        sol = next(best_first_search(p, search=tree_search))
        assert sol.state == goal
        assert p.nodes_expanded == pow(2, goal + 1) - 2
        assert p.goal_tests == pow(2, goal)


def test_best_first_search_with_heuristic():
    """
    Best heuristic is essentially depth first.
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(HeuristicEasyProblem(0, extra=goal))
        sol = next(best_first_search(p, search=tree_search))
        assert sol.state == goal
        assert p.nodes_expanded == goal*2
        assert p.goal_tests == goal+1


def test_iterative_best_first_tree_search():
    """
    Test iterative deepening tree search. When there is a perfect heuristic the
    cost is increased until the heuristic is included, then search proceeds
    directly to the solution.
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(HeuristicEasyProblem(0, extra=goal))
        sol = next(iterative_deepening_best_first_search(p,
                                                         search=tree_search))
        assert sol.state == goal
        assert p.nodes_expanded == goal*2
        assert p.goal_tests == goal+1


def test_iterative_deepening_best_first_search():
    """
    Without heuristic it is basically the same as iterative_deepening_search.
    (here is the case where we use graph search).
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(EasyProblem(0, extra=goal))
        sol = next(iterative_deepening_best_first_search(p,
                                                         search=graph_search))
        assert sol.state == goal
        assert p.nodes_expanded == sum([i*2 for i in range(1, goal+2)])-2
        assert p.goal_tests == sum([i+1 for i in range(1, goal+1)])+1


def test_beam1_tree_search():
    """
    Beam search with a width of 1 is like a depth first search, but with no
    backtracking.
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(EasyProblem(0, extra=goal))
        sol = next(beam_search(p, beam_width=1, graph_search=False))
        assert sol.state == goal
        assert p.nodes_expanded == goal*2
        assert p.goal_tests == goal+1


def test_beam2_tree_search():
    """
    Beam search with a width of 2 is slightly different. It is like a fusion of
    breadth and depth first searches.
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(EasyProblem(0, extra=goal))
        sol = next(beam_search(p, beam_width=2, graph_search=False))
        assert sol.state == goal
        assert p.nodes_expanded == 2 + (goal-1)*4
        assert p.goal_tests == 2 + (goal-1)*2


def test_beam2_graph_search():
    """
    like test_beam2_tree_search, but eliminates duplicate nodes
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(EasyProblem(0, extra=goal))
        sol = next(beam_search(p, beam_width=2, graph_search=True))
        assert sol.state == goal
        assert p.nodes_expanded == goal*2
        assert p.goal_tests == goal+1


def test_widening_beam_search():
    pass
