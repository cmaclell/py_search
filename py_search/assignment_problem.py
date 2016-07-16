from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division
from itertools import permutations
from random import normalvariate
from random import shuffle
from random import randint

from munkres import Munkres

from py_search.search import *

def random_matrix(n):
    """
    Generates an a list of list of floats (representing an n x n matrix) where
    the values have mean 0 and std 1.

    This is used as cost matrix for an assignment problem.
    """
    return [[normalvariate(0,1) for j in range(n)] for i in range(n)]

class TAssignmentProblem(Problem):

    def h(self, node):
        node.state
        costs, unassigned = node.extra

        empty_rows = [i for i,v in enumerate(node.state) if v is None]

        min_possible = 0
        for r in empty_rows:
            sub_c = [v for i, v in enumerate(costs[r]) if i in unassigned]
            min_possible += min(sub_c)

        return min_possible

    def node_value(self, node):
        return node.cost() + self.h(node)

    def successors(self, node):
        state = node.state
        costs, unassigned = node.extra

        for i,v in enumerate(state):
            if v is None:
                for u in unassigned:
                    new_state = tuple([u if i==j else k 
                                       for j,k in enumerate(state)])
                    new_unassigned = tuple([k for k in unassigned if k != u])
                    
                    c = node.cost() + costs[i][u]
                    yield Node(new_state, node, (i, u), c, extra=(costs,
                                                            new_unassigned))

    def goal_test(self, node):
        state = node.state
        return None not in state

class AssignmentProblem(OptimizationProblem):
    """
    This class represents an assignment problem and instantiates the successor
    and goal test functions necessary for conducting search. 
    """
    def node_value(self, node):
        """
        Function for computing the value of a node.
        """
        return node.cost()

    def random_successor(self, node):
        costs = node.extra[0]

        p = [0,0]
        p[0] = randint(0, len(node.state)-1)
        p[1] = p[0] 
        while p[0] == p[1]:
            p[1] = randint(0, len(node.state)-1)

        new_cost = node.cost()
        new_cost -= costs[p[0]][node.state[p[0]]]
        new_cost -= costs[p[1]][node.state[p[1]]]
        new_cost += costs[p[0]][node.state[p[1]]]
        new_cost += costs[p[1]][node.state[p[0]]]

        state = list(node.state)
        temp = state[p[0]]
        state[p[0]] = state[p[1]]
        state[p[1]] = temp

        return Node(tuple(state), node, p, new_cost, extra=node.extra)


    def successors(self, node):
        """
        Generates successor states by flipping each pair of assignments. 
        """
        costs = node.extra[0]

        for p in permutations(node.state, 2):
            new_cost = node.cost()
            new_cost -= costs[p[0]][node.state[p[0]]]
            new_cost -= costs[p[1]][node.state[p[1]]]
            new_cost += costs[p[0]][node.state[p[1]]]
            new_cost += costs[p[1]][node.state[p[0]]]

            state = list(node.state)
            temp = state[p[0]]
            state[p[0]] = state[p[1]]
            state[p[1]] = temp

            yield Node(tuple(state), node, p, new_cost, extra=node.extra)

def random_assignment(n):
    state = list(range(n))
    shuffle(state)
    return tuple(state)

def cost(assignment, costs):
    cost = 0.0
    for row, col in enumerate(assignment):
        cost += costs[row][col]
    return cost

def print_matrix(m):
    for row in m:
        print("\t".join(["%0.2f" % v for v in row]))

if __name__ == "__main__":

    n = 8
    costs = random_matrix(n)

    print()
    print("####################################################")
    print("Randomly generated square cost matrix (%i x %i)" % (n, n))
    print("####################################################")
    print_matrix(costs)

    print()
    print("####################################################")
    print("Optimial solution using Munkres/Hungarian Algorithm")
    print("####################################################")

    m = Munkres()
    indices = m.compute(costs)
    best = tuple([v[1] for v in indices])
    print("Munkres Solution:")
    print(best)
    print("Munkres Cost:")
    print(cost(best, costs))
    print()

    print("####################################")
    print("Local Search Optimization Techniques")
    print("####################################")

    initial = random_assignment(n)
    problem = AssignmentProblem(initial, initial_cost=cost(initial, costs),
                                extra=(costs,)) 
    print("Initial Assignment (randomly generated):")
    print(initial)
    print("Initial Assignment Cost:")
    print(problem.initial.cost())
    print()


    def beam_width2(problem):
        return beam_optimization(problem, beam_width=2)
    def annealing_2000steps(problem):
        return simulated_annealing_optimization(problem, limit=2000)

    compare_searches(problems=[problem],
                     searches=[hill_climbing_optimization ,beam_width2, 
                               annealing_2000steps])

    print()
    print("####################################")
    print("Tree Search Optimization Techniques")
    print("####################################")

    # TREE SEARCH APPROACH
    empty = tuple([None for i in range(len(costs))])
    unassigned = [i for i in range(len(costs))]

    new_costs = [[c - min(row) for c in row] for row in costs]
    min_c = [min([row[c] for row in costs]) for c,v in enumerate(costs[0])]
    new_costs = [[v - min_c[c] for c, v in enumerate(row)] for row in costs]

    tree_problem = TAssignmentProblem(empty, extra=(costs, unassigned)) 

    def tree_beam_width2(problem):
        return beam_search(problem, beam_width=2)

    print()
    compare_searches(problems=[tree_problem],
                     searches=[tree_beam_width2,
                               best_first_search])
