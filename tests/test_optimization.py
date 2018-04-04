"""
Tests for the optimization search techniques.
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from random import normalvariate
from random import choice

from py_search.base import Node
from py_search.base import Problem
from py_search.base import AnnotatedProblem
from py_search.optimization import hill_climbing
from py_search.optimization import local_beam_search
from py_search.optimization import simulated_annealing
from py_search.optimization import branch_and_bound


class PlateauProblem(Problem):

    def node_value(self, node):
        space = [-5, -5, -5, -6, -6, -6, -2, -2, -2, -8, -10, -10, -11]
        return space[node.state]

    def random_node(self):
        v = choice(list(i for i in range(11)))
        v = choice([v, 12])
        print("RANDOM NODE %s" % v)
        return Node(v)

    def successors(self, node):
        v = node.state
        yield node

        if v > 0:
            yield Node(v - 1)
        if v < 11:
            yield Node(v + 1)

    def random_successor(self, node):
        v = node.state
        choices = []
        if v > 0:
            choices.append(v-1)
        if v < 11:
            choices.append(v+1)
        return Node(choice(choices))


class PlateauProblemWithGoal(PlateauProblem):

    def goal_test(self, node, goal=None):
        return (node.state == 3 or node.state == 4 or node.state == 5 or
                node.state == 12)


class HillProblem(Problem):

    def node_value(self, node):
        return abs(node.state - self.goal.state)

    def successors(self, node):
        for i in range(100):
            v = node.state + normalvariate(0, 1)
            yield Node(v, node, 'expand', extra=node.extra)

    def random_successor(self, node):
        v = node.state + normalvariate(0, 1)
        return Node(v, node, 'expand', extra=node.extra)

    def goal_test(self, state_node, goal_node=None):
        if goal_node is None:
            goal_node = self.goal
        return abs(state_node.state - goal_node.state) <= 0.1


class HillProblemNoGoalTest(HillProblem):

    def goal_test(self, state_node, goal_node=None):
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


def test_hill_climbing():
    initial = 0
    goal = 10
    limits = (-goal, goal)
    p = AnnotatedProblem(EasyProblem(initial, initial_cost=initial,
                                     extra=limits))
    sol = next(hill_climbing(p, graph=False))
    assert abs(sol.state_node.state - limits[0]) <= 0.1

    p2 = HillProblem(initial, goal=goal, initial_cost=initial, extra=limits)
    sol = next(hill_climbing(p2))
    assert abs(sol.state_node.state - goal) <= 0.1

    p3 = AnnotatedProblem(HillProblem(initial, goal=initial,
                                      initial_cost=initial, extra=limits))
    sol = next(hill_climbing(p3))
    assert p3.nodes_expanded == 0
    assert p3.goal_tests == 1
    assert abs(sol.state_node.state - initial) <= 0.1

    p4 = AnnotatedProblem(PlateauProblem(initial))
    sol = next(hill_climbing(p4, random_restarts=3))

    p5 = AnnotatedProblem(PlateauProblemWithGoal(initial))
    sols = list(hill_climbing(p5, random_restarts=3))

    # assert sol.state == 0
    # initial = nQueens(5)
    # initial.randomize()
    # cost = initial.num_conflicts()
    # p4 = LocalnQueensProblem(initial, initial_cost=cost)
    # solutions = list(hill_climbing(p4, random_restarts=1))
    # assert abs(sol.state - goal) <= 0.1


def test_local_beam_search():
    initial = 0
    goal = 10
    limits = (-goal, goal)
    p = AnnotatedProblem(EasyProblem(initial, initial_cost=initial,
                                     extra=limits))
    sol = next(local_beam_search(p, graph=False))
    assert abs(sol.state_node.state - limits[0]) <= 0.1

    p2 = HillProblem(initial, goal=goal, initial_cost=initial, extra=limits)
    sol = next(local_beam_search(p2))
    assert abs(sol.state_node.state - goal) <= 0.1

    p3 = HillProblemNoGoalTest(initial, goal=goal, initial_cost=initial,
                               extra=limits)
    sol = next(local_beam_search(p3))
    assert abs(sol.state_node.state - goal) <= 0.1

    p4 = AnnotatedProblem(HillProblem(initial, goal=initial,
                                      initial_cost=initial, extra=limits))
    sol = next(local_beam_search(p4))
    assert p4.nodes_expanded == 0
    assert p4.goal_tests == 1
    assert abs(sol.state_node.state - initial) <= 0.1

    p5 = AnnotatedProblem(PlateauProblem(initial))
    sol = next(local_beam_search(p5, beam_width=2))
    # assert sol.state == 0


def test_simulated_annealing():
    initial = 0
    goal = 10
    limits = (-goal, goal)
    p = AnnotatedProblem(EasyProblem(initial, initial_cost=initial,
                                     extra=limits))
    sol = next(simulated_annealing(p))
    assert abs(sol.state_node.state - limits[0]) <= 0.1

    p2 = HillProblem(initial, goal=goal, initial_cost=initial, extra=limits)
    sol = next(simulated_annealing(p2))
    assert abs(sol.state_node.state - goal) <= 0.1

    p3 = AnnotatedProblem(HillProblem(initial, goal=initial,
                                      initial_cost=initial, extra=limits))
    sol = next(simulated_annealing(p3))
    assert p3.nodes_expanded == 0
    assert p3.goal_tests == 1
    assert abs(sol.state_node.state - initial) <= 0.1

    p4 = HillProblem(initial, goal=goal, initial_cost=initial,
                     extra=limits)
    sol = next(simulated_annealing(p4, limit=2))
    # because of the tight limit, very very unlikely it will find the goal
    # assert abs(sol.state_node.state - initial) > 0.01


def test_branch_and_bound():
    initial = 0
    goal = 10
    limits = (-goal, goal)
    p = AnnotatedProblem(EasyProblem(initial, initial_cost=initial,
                                     extra=limits))
    sol = next(branch_and_bound(p))
    assert abs(sol.state_node.state - limits[0]) <= 0.1

    sol = next(branch_and_bound(p, graph=False))
    assert abs(sol.state_node.state - limits[0]) <= 0.1

    p2 = HillProblem(initial, goal=goal, initial_cost=initial, extra=limits)

    sol = next(branch_and_bound(p2, graph=False))
    assert abs(sol.state_node.state - goal) <= 0.1

    p3 = AnnotatedProblem(HillProblem(initial, goal=initial,
                                      initial_cost=initial, extra=limits))
    sol = next(branch_and_bound(p3))
    assert p3.nodes_expanded == 0
    assert p3.goal_tests == 1
    assert abs(sol.state_node.state - initial) <= 0.1
