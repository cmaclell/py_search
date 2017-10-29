"""
Tests for the uninformed search techniques.
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from math import pow

from py_search.base import Node
from py_search.base import Problem
from py_search.base import AnnotatedProblem
from py_search.uninformed import depth_first_search
from py_search.uninformed import breadth_first_search
from py_search.uninformed import iterative_deepening_search


class EasyProblem(Problem):

    def successors(self, node):
        yield Node(node.state+1, node, 'expand', node.cost()+1)
        yield Node(node.state+1, node, 'expand', node.cost()+1)


class EasyProblem2(Problem):

    def successors(self, node):
        yield Node(node.state, node, 'expand', node.cost()+1)
        yield Node(node.state, node, 'expand', node.cost()+1)


def test_depth_first_tree_search():
    """
    Test depth first tree search (i.e., with duplicates).
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(EasyProblem(0, goal))
        sol = next(depth_first_search(p, search="tree"))
        assert sol.state == goal
        assert p.nodes_expanded == goal*2
        assert p.goal_tests == goal+1


def test_depth_first_graph_search():
    """
    depth-first graph and tree search are the same on this problem.
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(EasyProblem(0, goal))
        sol = next(depth_first_search(p, search="graph"))
        assert sol.state == goal
        assert p.nodes_expanded == goal*2
        assert p.goal_tests == goal+1

        p2 = AnnotatedProblem(EasyProblem2(0, goal))
        try:
            next(depth_first_search(p2, search="graph"))
            assert False
        except StopIteration:
            assert p2.nodes_expanded == 2
            assert p2.goal_tests == 1


def test_breadth_first_tree_search():
    """
    Test breadth first tree search (i.e., with duplicates).
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(EasyProblem(0, goal))
        sol = next(breadth_first_search(p, search="tree"))
        assert sol.state == goal
        assert p.nodes_expanded == pow(2, goal+1)-2
        assert p.goal_tests == pow(2, goal)


def test_breadth_first_graph_search():
    """
    Test breadth first graph search (i.e., no duplicates). For this test
    problem it performs similar to breadth first.
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(EasyProblem(0, goal))
        sol = next(breadth_first_search(p, search="graph"))
        assert sol.state == goal
        assert p.nodes_expanded == goal*2
        assert p.goal_tests == goal+1


def test_iterative_deepening_tree_search():
    """
    Test iterative deepening tree search.
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(EasyProblem(0, goal))
        sol = next(iterative_deepening_search(p, search="tree"))
        assert sol.state == goal
        assert (p.nodes_expanded == sum([pow(2, i+1)-2
                                         for i in range(1, goal)]) + (goal*2))
        assert (p.goal_tests == sum([pow(2, i+1)-2 for i in range(1, goal)]) +
                (goal*2) + 1)


def test_iterative_deepening_graph_search():
    """
    Test iterative deepening graph search.
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(EasyProblem(0, goal))
        sol = next(iterative_deepening_search(p, search="graph"))
        assert sol.state == goal
        assert p.nodes_expanded == sum([i*2 for i in range(1, goal+1)])
        assert p.goal_tests == sum([i+1 for i in range(1, goal+1)])+1
