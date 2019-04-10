"""
Tests for the uninformed search techniques.
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from math import pow

import pytest

from py_search.base import Node
from py_search.base import GoalNode
from py_search.base import Problem
from py_search.base import AnnotatedProblem
from py_search.uninformed import tree_search
from py_search.uninformed import graph_search
from py_search.uninformed import depth_first_search
from py_search.uninformed import breadth_first_search
from py_search.uninformed import iterative_deepening_search
from py_search.uninformed import iterative_sampling
from py_search.utils import compare_searches


class ImpossibleProblem(Problem):

    def successors(self, node):
        yield Node(node.state, node, 'expand', node.cost()+1)
        return


class EasyProblem(Problem):

    def successors(self, node):
        yield Node(node.state+1, node, 'expand', node.cost()+1)
        yield Node(node.state+1, node, 'expand', node.cost()+1)

    def predecessors(self, node):
        yield GoalNode(node.state-1, node, 'expand', node.cost()+1)
        yield GoalNode(node.state-1, node, 'expand', node.cost()+1)

    def goal_test(self, s, g):
        return super(EasyProblem, self).goal_test(s, g)


class EasyProblem2(Problem):

    def successors(self, node):
        yield Node(node.state, node, 'expand', node.cost()+1)
        yield Node(node.state, node, 'expand', node.cost()+1)


def search_wrapper(search, p, search_type):
    return next(search(p, search=search_type))


def test_base_search_exceptions():
    ep = EasyProblem(0, 5)
    try:
        next(tree_search(ep, None, None))
        assert False
    except Exception:
        pass

    try:
        next(graph_search(ep, None, None))
        assert False
    except Exception:
        pass


def test_compare_problems():
    ep = EasyProblem(0, 5)
    ip = ImpossibleProblem(0, 5)
    compare_searches([ep, ip], [depth_first_search, breadth_first_search])


def test_solution_node():
    ep = EasyProblem(0, 8)
    sol1 = next(depth_first_search(ep))
    assert sol1.depth() == 8
    assert sol1.path() == tuple(['expand'] * 8)

    assert str(sol1) == ("StateNode={State: 8, Extra: None}, "
                         "GoalNode={State: 8, Extra: None}")
    assert repr(sol1) == "SolutionNode(Node(8), GoalNode(8))"
    assert hash(sol1) == hash((8, 8))

    sol2 = next(breadth_first_search(ep, forward=True,
                                     backward=True))
    assert sol2.depth() == 8
    print(sol2.path())
    assert sol2.path() == tuple(['expand'] * 8)
    assert sol2.goal_node.path() == tuple(['expand'] * 4)

    assert str(sol2) == ("StateNode={State: 4, Extra: None}, "
                         "GoalNode={State: 4, Extra: None}")
    assert repr(sol2) == "SolutionNode(Node(4), GoalNode(4))"
    assert hash(sol2) == hash((4, 4))

    assert sol1 == sol1
    assert sol1 != sol2


def test_depth_first_tree_search():
    """
    Test depth first tree search (i.e., with duplicates).
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(EasyProblem(0, goal))
        sol = next(depth_first_search(p, graph=False))
        assert sol.state_node.state == goal
        assert p.nodes_expanded == goal*2
        assert p.goal_tests == goal+1

        p = AnnotatedProblem(EasyProblem(0, goal))
        sol = next(depth_first_search(p, graph=False, forward=False,
                                      backward=True))
        assert sol.state_node == sol.goal_node
        assert p.nodes_expanded == goal*2
        assert p.goal_tests == goal+1

    try:
        p = EasyProblem(0, 10)
        next(depth_first_search(p, graph=False, depth_limit=5))
        assert False
    except StopIteration:
        pass

    try:
        p = EasyProblem(0, 10)
        next(depth_first_search(p, graph=False, forward=False, backward=True,
                                depth_limit=5))
        assert False
    except StopIteration:
        pass


def test_depth_first_graph_search():
    """
    depth-first graph and tree search are the same on this problem.
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(EasyProblem(0, goal))
        sol = next(depth_first_search(p, graph=True))
        assert sol.state_node.state == goal
        assert p.nodes_expanded == goal*2
        assert p.goal_tests == goal+1

        p = AnnotatedProblem(EasyProblem(0, goal))
        sol = next(depth_first_search(
            p, graph=True, forward=False, backward=True))
        assert sol.state_node == sol.goal_node
        assert p.nodes_expanded == goal*2
        assert p.goal_tests == goal+1

        p2 = AnnotatedProblem(EasyProblem2(0, goal))
        try:
            next(depth_first_search(p2, graph=True))
            assert False
        except StopIteration:
            assert p2.nodes_expanded == 2
            assert p2.goal_tests == 1

    try:
        p = EasyProblem(0, 10)
        next(depth_first_search(p, graph=True, depth_limit=5))
        assert False
    except StopIteration:
        pass

    try:
        p = EasyProblem(0, 10)
        next(depth_first_search(p, graph=True, forward=False, backward=True,
                                depth_limit=5))
        assert False
    except StopIteration:
        pass


def test_breadth_first_tree_search():
    """
    Test breadth first tree search (i.e., with duplicates).
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(EasyProblem(0, goal))
        sol = next(breadth_first_search(p, graph=False))
        assert sol.state_node.state == goal
        assert p.nodes_expanded == pow(2, goal+1)-2
        assert p.goal_tests == pow(2, goal)

        p = AnnotatedProblem(EasyProblem(0, goal))
        sol = next(breadth_first_search(p, graph=False,
                                        forward=False, backward=True))
        assert sol.state_node == sol.goal_node
        assert p.nodes_expanded == pow(2, goal+1)-2
        assert p.goal_tests == pow(2, goal)


def test_breadth_first_graph_search():
    """
    Test breadth first graph search (i.e., no duplicates). For this test
    problem it performs similar to breadth first.
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(EasyProblem(0, goal))
        sol = next(breadth_first_search(p, graph=True))
        assert sol.state_node.state == goal
        assert p.nodes_expanded == goal*2
        assert p.goal_tests == goal+1

        p = AnnotatedProblem(EasyProblem(0, goal))
        sol = next(breadth_first_search(p, graph=True,
                                        forward=False, backward=True))
        assert sol.state_node == sol.goal_node
        assert p.nodes_expanded == goal*2
        assert p.goal_tests == goal+1


def test_iterative_deepening_tree_search():
    """
    Test iterative deepening tree search.
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(EasyProblem(0, goal))
        sol = next(iterative_deepening_search(p, graph=False))
        assert sol.state_node.state == goal
        assert (p.nodes_expanded == sum([pow(2, i+1)-2
                                         for i in range(1, goal)]) + (goal*2))
        assert (p.goal_tests == sum([pow(2, i+1)-2 for i in range(1, goal)]) +
                (goal*2) + 1)

    p = EasyProblem(0, 10)
    try:
        next(iterative_deepening_search(p, graph=False, max_depth_limit=5))
        assert False
    except StopIteration:
        pass


def test_iterative_deepening_graph_search():
    """
    Test iterative deepening graph search.
    """
    for goal in range(1, 10):
        p = AnnotatedProblem(EasyProblem(0, goal))
        sol = next(iterative_deepening_search(p, graph=True))
        assert sol.state_node.state == goal
        assert p.nodes_expanded == sum([i*2 for i in range(1, goal+1)])
        assert p.goal_tests == sum([i+1 for i in range(1, goal+1)])+1

    p = EasyProblem(0, 10)
    try:
        next(iterative_deepening_search(p, graph=True, max_depth_limit=5))
        assert False
    except StopIteration:
        pass


def test_iterative_sampling_search():
    """
    Test iterative sampling search.
    """
    for goal in range(1, 10):
        p = EasyProblem(0, goal)
        sol = next(iterative_sampling(p, depth_limit=goal+1))
        assert sol.state_node.state == goal

        if goal == 1:
            isg = iterative_sampling(p, max_samples=1, depth_limit=1)
            next(isg)
            with pytest.raises(StopIteration):
                next(isg)
        elif goal > 1:
            with pytest.raises(StopIteration):
                next(iterative_sampling(p, max_samples=1, depth_limit=1))


def test_bidirectional_tree_search():
    for goal in range(1, 14):
        p = AnnotatedProblem(EasyProblem(0, goal))
        sol = next(breadth_first_search(p, graph=False, forward=True,
                                        backward=True))
        assert sol.state_node == sol.goal_node
        if goal % 2 == 0:
            assert p.nodes_expanded == 2 * (pow(2, goal/2 + 1) - 2)
            assert p.goal_tests == pow(2, goal)
        else:
            assert p.nodes_expanded == pow(2, goal//2+2) - 2
            # assert p.goal_tests == pow(2, goal-1) + 1

        # if goal > 1:
        #     assert p.goal_tests == pow(2, goal) - 1
