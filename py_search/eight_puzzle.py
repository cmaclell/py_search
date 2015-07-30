from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division
import random

from py_search.search import *

class EightPuzzle:
    """
    An eight puzzle class that can be used to test. 
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

    def copy(self):
        new = EightPuzzle()
        new.state = tuple([i for i in self.state])
        return new

    def randomize(self, num_shuffles):
        state = [0,1,2,3,4,5,6,7,8]
        self.state = tuple(state)

        for i in range(num_shuffles):
            self.executeAction(random.choice([a for a in self.legalActions()]))
 
    def __repr__(self):
        return str(self)

    def __str__(self):
        return "%i%i%i\n%i%i%i\n%i%i%i" % (self.state[0], self.state[1],
                                           self.state[2], self.state[3],
                                           self.state[4], self.state[5],
                                           self.state[6], self.state[7],
                                           self.state[8])

    def executeAction(self, action):
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

    def heuristic(self, state):
        """
        The misplaced tiles heuristic.
        """
        goal = EightPuzzle()
        h = 0
        for i,v in enumerate(state.state):
            if state.state[i] != goal.state[i]:
                h += 1
        return h

    def successor(self, node):
        """
        Computes successors and computes the value of the node as cost +
        heuristic, which yields A* search when using best first search.
        """
        for action in node.state.legalActions():
            new_state = node.state.copy()
            new_state.executeAction(action)
            cost = node.cost + 1
            h = self.heuristic(new_state)
            yield Node(new_state, node, action, cost, 
                       cost + h, node.depth+1)

    def goal_test(self, node):
        """
        Check if the goal state has been reached.
        """
        goal = EightPuzzle()
        return node.state == goal

class NoHeuristic(EightPuzzleProblem):
    def heuristic(self, node):
        return 0

if __name__ == "__main__":

    puzzle = EightPuzzle()
    puzzle.randomize(30)
    #puzzle.executeAction('left')
    #puzzle.executeAction('up')
    #puzzle.executeAction('up')

    initial = puzzle
    print("INITIAL:")
    print(puzzle)
    print()

    compare_searches(problems=[EightPuzzleProblem(initial)],
                     searches=[best_first_search,
                               iterative_deepening_best_first_search,
                               widening_beam_search])
