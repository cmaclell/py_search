from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division
from random import choice

from py_search.base import Problem
from py_search.base import Node
from py_search.uninformed import depth_first_search
from py_search.uninformed import breadth_first_search
from py_search.uninformed import iterative_deepening_search
from py_search.informed import best_first_search
from py_search.informed import iterative_deepening_best_first_search
from py_search.informed import widening_beam_search
from py_search.utils import compare_searches

class EightPuzzle:
    """
    An eight puzzle class that can be used to test different search algorithms.
    When first created the puzzle is in the solved state. 
    """

    def __init__(self):
        self.state = (0,1,2,3,4,5,6,7,8)

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        if isinstance(other, EightPuzzle):
            return self.state == other.state
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "%i%i%i\n%i%i%i\n%i%i%i" % (self.state[0], self.state[1],
                                           self.state[2], self.state[3],
                                           self.state[4], self.state[5],
                                           self.state[6], self.state[7],
                                           self.state[8])

    def copy(self):
        """
        Makes a deep copy of an EightPuzzle object.
        """
        new = EightPuzzle()
        new.state = tuple([i for i in self.state])
        return new

    def randomize(self, num_shuffles):
        """
        Randomizes an EightPuzzle by executing a random action `num_suffles`
        times.
        """
        state = [0,1,2,3,4,5,6,7,8]
        self.state = tuple(state)

        for i in range(num_shuffles):
            self.executeAction(choice([a for a in self.legalActions()]))
 
    def executeAction(self, action):
        """
        Executes an action to the EightPuzzle object.

        :param action: the action to execute
        :type action: "up", "left", "right", or "down"
        """
        zeroIndex = self.state.index(0)
        successor = list(self.state)

        if action == 'up':
            successor[zeroIndex] = successor[zeroIndex + 3]
            successor[zeroIndex + 3] = 0
        elif action == 'left':
            successor[zeroIndex] = successor[zeroIndex + 1]
            successor[zeroIndex + 1] = 0
        elif action == 'right':
            successor[zeroIndex] = successor[zeroIndex - 1]
            successor[zeroIndex - 1] = 0
        elif action == 'down':
            successor[zeroIndex] = successor[zeroIndex - 3]
            successor[zeroIndex - 3] = 0

        self.state = tuple(successor)

    def legalActions(self):
        """
        Returns an iterator to the legal actions that can be executed in the
        current state.
        """
        zeroIndex = self.state.index(0)

        if zeroIndex in set([0,1,2,3,4,5]):
            yield "up"
        if zeroIndex in set([0,3,6,1,4,7]):
            yield "left"
        if zeroIndex in set([2,5,8,1,4,7]):
            yield "right"
        if zeroIndex in set([3,4,5,6,7,8]):
            yield "down"

class EightPuzzleProblem(Problem):
    """
    This class wraps around an Eight Puzzle object and instantiates the
    successor and goal test functions necessary for conducting search. 
    
    This class also implements an heuristic function which is used to compute
    the value for each successor as cost to node + heuristic estimate of
    distance to goal. This yield A* search when used with best first search or
    a more greedy variant when used with Beam Search.
    """

    def misplaced_tile_heuristic(self, state):
        """
        The misplaced tiles heuristic.
        """
        goal = EightPuzzle()
        h = 0
        for i,v in enumerate(state.state):
            if state.state[i] != goal.state[i]:
                h += 1
        return h

    def node_value(self, node):
        """
        The function used to compute the value of a node.
        """
        return node.cost() + self.misplaced_tile_heuristic(node.state)

    def successors(self, node):
        """
        Computes successors and computes the value of the node as cost +
        heuristic, which yields A* search when using best first search.
        """
        for action in node.state.legalActions():
            new_state = node.state.copy()
            new_state.executeAction(action)
            path_cost = node.cost() + 1
            yield Node(new_state, node, action, path_cost)

    def goal_test(self, node):
        """
        Check if the goal state has been reached.
        """
        goal = EightPuzzle()
        return node.state == goal

class NoHeuristic(EightPuzzleProblem):
    """
    A variation on the Eight Puzzle Problem that has a heuristic for 0. This
    yields something equivelent to dijkstra's algorithm when used with best
    first search and a more greedy variant when used with Beam Search.
    """

    def node_value(self, node):
        return node.cost()

if __name__ == "__main__":

    puzzle = EightPuzzle()
    puzzle.randomize(10)

    initial = puzzle
    print("Puzzle being solved:")
    print(puzzle)
    print()

    compare_searches(problems=[EightPuzzleProblem(initial)],
                     searches=[depth_first_search,
                               breadth_first_search,
                               iterative_deepening_search,
                               best_first_search,
                               iterative_deepening_best_first_search,
                               widening_beam_search])
