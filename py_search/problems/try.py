from py_search.problems.eight_puzzle import EightPuzzleProblem, EightPuzzle
from py_search.uninformed import breadth_first_search
from py_search.informed import best_first_search, near_optimal_front_to_end_bidirectional_search
from py_search.utils import compare_searches

puzzle = EightPuzzle()
puzzle.randomize(100)

initial = puzzle
print("Puzzle being solved:")
print(puzzle)
print()

problem = EightPuzzleProblem(initial, EightPuzzle())


def bidirectional_breadth_first_search(problem):
    return breadth_first_search(problem, forward=True, backward=True)


compare_searches(problems=[EightPuzzleProblem(initial, EightPuzzle()) for _ in range(3)],
                 searches=[best_first_search,
                           bidirectional_breadth_first_search,
                           near_optimal_front_to_end_bidirectional_search, ])
