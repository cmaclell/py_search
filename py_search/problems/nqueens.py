from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from random import shuffle

from py_search.base import Problem
from py_search.base import Node
from py_search.uninformed import depth_first_search
from py_search.uninformed import breadth_first_search
from py_search.informed import best_first_search
from py_search.informed import iterative_deepening_best_first_search
from py_search.informed import beam_search
from py_search.optimization import hill_climbing
from py_search.optimization import local_beam_search
from py_search.optimization import simulated_annealing

from py_search.utils import compare_searches

class nQueens:
    """
    An nQueens puzzle object
    """

    def __init__(self, n):
        self.n = n
        self.state = tuple([None for i in range(n)])

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        if isinstance(other, nQueens):
            return self.state == other.state
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self)

    def __str__(self):
        output = ""
        for c in self.state:
            if c is None:
                output += "|" + "|".join([" " for i in range(self.n)]) + "|\n"
            else:
                 
                output += "|" + "|".join([" " for i in range(c)] + ["Q"] + [" " for i in range(self.n-c-1)]) + "|\n"
        return output

    def copy(self):
        """
        Makes a deep copy of an nQueens object.
        """
        new = nQueens(self.n)
        new.state = tuple([i for i in self.state])
        return new

    def randomize(self):
        """
        Randomizes an nQueens by shuffling a list of row to columns
        assignments.
        """
        state = [i for i in range(self.n)]
        shuffle(state)
        self.state = tuple(state)

    def num_conflicts(self):
        """
        Returns a count of the number of conflicts. First checks if there are
        column conflicts (row conflicts are impossible because of
        representation). Then checks for diagonals. 
        """
        conflicts = 0
        for r1 in range(len(self.state)):
            c1 = self.state[r1]
            if c1 is None:
                continue
            for r2 in range(r1+1, len(self.state)):
                c2 = self.state[r2]
                if c2 is None:
                    continue
                if c1 == c2:
                    conflicts += 1
                if r2 - r1 == c2 - c1:
                    conflicts += 1
        return conflicts

class nQueensProblem(Problem):
    """
    A class that wraps around the nQueens object. This version of the problem
    starts with an empty board and then progressively adds queens. 
    """
    def node_value(self, node):
        """
        The function used to compute the value of a node.
        """
        return node.state.num_conflicts()

    def successors(self, node):
        """
        Generate all possible next queen states.
        """
        free_columns = set([i for i in range(node.state.n)]) - set(node.state.state)

        for row, col in enumerate(node.state.state):
            if col is None:
                for nc in free_columns:
                    new_state = node.state.copy()
                    ns = [i for i in node.state.state]
                    ns[row] = nc
                    new_state.state = tuple(ns)
                    yield Node(new_state, node, ('add-queen', row, nc),
                               node.cost()+1)

    def goal_test(self, node):
        """
        Check if the goal state (i.e., no queen conflicts) has been reached.
        """
        return (len(set(node.state.state) - set([None])) == node.state.n and
                node.state.num_conflicts() == 0)

class LocalnQueensProblem(Problem):
    """
    A class that wraps around the nQueens object. This version of the problem
    starts with an empty board and then progressively adds queens. 
    """
    def node_value(self, node):
        return node.state.num_conflicts()

    def successors(self, node):
        """
        Generate all permutations of rows.
        """
        for r1 in range(len(node.state.state)):
            c1 = node.state.state[r1]

            for r2 in range(r1+1, len(node.state.state)):
                c2 = node.state.state[r2]

                new_state = node.state.copy()
                ns = [i for i in node.state.state]
                ns[r1] = c2
                ns[r2] = c1
                new_state.state = tuple(ns)
                yield Node(new_state, node, ('swap', (r1,c1), (r2,c2)))

    def random_node(self):
        nq_state = self.initial.state.copy()
        nq_state.randomize()
        return Node(nq_state, None, None)

    def random_successor(self, node):
        """
        Generate all permutations of rows.
        """
        rows = [i for i in range(node.state.n)]
        shuffle(rows)

        r1 = rows[0]
        c1 = node.state.state[r1]
        r2 = rows[1]
        c2 = node.state.state[r2]

        new_state = node.state.copy()
        ns = [i for i in node.state.state]
        ns[r1] = c2
        ns[r2] = c1
        new_state.state = tuple(ns)
        return Node(new_state, node, ('swap', (r1,c1), (r2,c2)))

    def goal_test(self, node):
        """
        Check if the goal state (i.e., no queen conflicts) has been reached.
        """
        return (len(set(node.state.state) - set([None])) == node.state.n and
                node.state.num_conflicts() == 0)

if __name__ == "__main__":

    print("###################")
    print("BACKTRACKING SEARCH")
    print("###################")

    initial = nQueens(5)
    print("Empty %i-Queens Problem" % initial.n)
    print(initial)
    print()

    compare_searches(problems=[nQueensProblem(initial)],
                     searches=[depth_first_search,
                               breadth_first_search,
                               best_first_search,
                               iterative_deepening_best_first_search,
                               beam_search])
    print()

    print("##########################")
    print("LOCAL SEARCH / OPTIMZATION")
    print("##########################")

    initial = nQueens(10)
    initial.randomize()
    print("Random %i-Queens Problem" % initial.n)
    print(initial)
    print(initial.num_conflicts())
    print()

    def beam2(problem):
        return local_beam_search(problem, beam_width=2, cost_limit=0)

    def steepest_hill(problem):
        return hill_climbing(problem, cost_limit=0)

    def annealing(problem):
        size = problem.initial.state.n
        n_neighbors = (size * (size-1)) // 2
        return simulated_annealing(problem, cost_limit=0,
                                   initial_temp=1.8,
                                   temp_length=n_neighbors)

    def greedy_annealing(problem):
        size = problem.initial.state.n
        n_neighbors = (size * (size-1)) // 2
        return simulated_annealing(problem, cost_limit=0,
                                   initial_temp=0,
                                   temp_length=n_neighbors)

    compare_searches(problems=[LocalnQueensProblem(initial)],
                     searches=[best_first_search,
                               beam2,
                               steepest_hill,
                               greedy_annealing,
                               annealing])
    print()

    initial = nQueens(50)
    initial.randomize()
    print("Random %i-Queens Problem" % initial.n)
    print(initial)
    print(initial.num_conflicts())
    print()

    compare_searches(problems=[LocalnQueensProblem(initial)],
                     searches=[steepest_hill,
                               greedy_annealing,
                               annealing])
