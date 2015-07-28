from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import random

from py_search.search import SearchNode
from py_search.search import BeamGS

class EightPuzzle:

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

    def randomize(self):
        state = [0,1,2,3,4,5,6,7,8]
        self.state = tuple(state)

        for i in range(100):
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

def successorFn8Puzzle(node):
    for action in node.state.legalActions():
        newState = node.state.copy()
        newState.executeAction(action)
        yield Node(newState, node, action, node.cost+1, node.depth+1)

def heuristicFn8Puzzle(node):
    """
    Currently the misplaced tile count
    """
    goal = EightPuzzle()
    h = 0
    for i,v in enumerate(node.state.state):
        if node.state.state[i] != goal.state[i]:
            h += 1
    return h

def goalTestFn8Puzzle(node):
    goal = EightPuzzle()
    return node.state == goal

if __name__ == "__main__":

    puzzle = EightPuzzle()
    puzzle.randomize()
    #puzzle.executeAction('left')
    #puzzle.executeAction('up')
    #puzzle.executeAction('up')

    initial = puzzle
    print("INITIAL:")
    print(puzzle)
    print()

    #print("BREADTH FIRST GRAPH SEARCH")
    #sol = next(BreadthFGS(Node(initial), successorFn8Puzzle, goalTestFn8Puzzle))
    #print("Solution Length = %i" % len(sol.getSolution()))
    #print()

    #print("DEPTH FIRST GRAPH SEARCH")
    #sol = next(DepthFGS(Node(initial), successorFn8Puzzle, goalTestFn8Puzzle))
    #print("Solution Length = %i" % len(sol.getSolution()))
    #print()
    #
    #print("BEST FIRST GRAPH SEARCH")
    #sol = next(BestFGS(Node(initial), successorFn8Puzzle, goalTestFn8Puzzle,
    #              heuristicFn8Puzzle))
    #print("Solution Length = %i" % len(sol.getSolution()))
    #print()

    print("BEAM GRAPH SEARCH")
    sol = next(BeamGS(SearchNode(initial), successorFn8Puzzle, goalTestFn8Puzzle,
                  heuristicFn8Puzzle, 10))
    print("Solution Length = %i" % len(sol.getSolution()))
    print()

#    print("ITERATIVE DEEPENING DEPTH FIRST SEARCH")
#    sol = next(IDDFS(Node(initial), successorFn8Puzzle, goalTestFn8Puzzle))
#    print("Solution Length = %i" % len(sol.getSolution()))
#    print()
#
    #print("ITERATIVE DEEPENING BEST FIRST SEARCH")
    #sol = next(IDBFS(Node(initial), successorFn8Puzzle, goalTestFn8Puzzle,
    #              heuristicFn8Puzzle))
    #print("Solution Length = %i" % len(sol.getSolution()))
    #print()

    #print("BEAM SEARCH")
    #sol = next(BeamS(Node(initial), successorFn8Puzzle, goalTestFn8Puzzle,
    #              heuristicFn8Puzzle))
    #print("Solution Length = %i" % len(sol.getSolution()))
    #print()

    #print("BREADTH FIRST SEARCH")
    #sol = next(BreadthFS(Node(initial), successorFn8Puzzle, goalTestFn8Puzzle))
    #print("Solution Length = %i" % len(sol.getSolution()))
    #print()

    #print("DEPTH FIRST SEARCH")
    #sol = next(DepthFS(Node(initial), successorFn8Puzzle, goalTestFn8Puzzle))
    #print("Solution Length = %i" % len(sol.getSolution()))
    #print()
