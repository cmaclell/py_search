Eight Puzzle Search Example
===========================

.. ipython::

    In [1]: from py_search.problems.eight_puzzle import EightPuzzle
       ...: from py_search.problems.eight_puzzle import EightPuzzleProblem
       ...: from py_search.utils import compare_searches
       ...: from py_search.uninformed import depth_first_search
       ...: from py_search.uninformed import breadth_first_search
       ...: from py_search.uninformed import iterative_deepening_search
       ...: from py_search.informed import best_first_search
       ...: from py_search.informed import iterative_deepening_best_first_search
       ...: from py_search.informed import widening_beam_search
       ...: puzzle = EightPuzzle()
       ...: puzzle.randomize(20)
       ...: initial = puzzle
       ...: print("Eight puzzle being solved:")
       ...: print(puzzle)
       ...: print()
       ...:
       ...: compare_searches(problems=[EightPuzzleProblem(initial)], 
       ...:                  searches=[depth_first_search,
       ...:                            breadth_first_search, 
       ...:                            iterative_deepening_search, 
       ...:                            best_first_search, 
       ...:                            iterative_deepening_best_first_search, 
       ...:                            widening_beam_search])
    
