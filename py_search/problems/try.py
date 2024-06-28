from py_search.problems.eight_puzzle import EightPuzzleProblem, EightPuzzle
from py_search.problems.missionaries_and_cannibals import MissionariesAndCannibals
from py_search.uninformed import breadth_first_search
from py_search.informed import best_first_search, near_optimal_front_to_end_bidirectional_search
from py_search.utils import compare_searches


def bidirectional_breadth_first_search(problem):
    return breadth_first_search(problem, forward=True, backward=True)


compare_searches(problems=[MissionariesAndCannibals(m, c, b)
                           for m in range(10000, 10020, 10)
                           for c in range(10000, 10020, 10)
                           for b in range(4, 8, 2)
                           ]
                 ,
                 searches=[
                     best_first_search,
                     bidirectional_breadth_first_search,
                     near_optimal_front_to_end_bidirectional_search,
                 ])
