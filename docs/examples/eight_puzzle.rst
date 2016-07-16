Eight Puzzle Search Example
===========================

.. ipython::

    In [1]: from py_search.eight_puzzle import EightPuzzle
       ...: from py_search.eight_puzzle import EightPuzzleProblem
       ...: from py_search.search import compare_searches
       ...: from py_search.search import best_first_search
       ...: from py_search.search import iterative_deepening_best_first_search
       ...: from py_search.search import widening_beam_search
       ...: puzzle = EightPuzzle()
       ...: puzzle.randomize(20)
       ...: initial = puzzle
       ...: print("Eight puzzle being solved:")
       ...: print(puzzle)
       ...: print()
       ...:
       ...: compare_searches(problems=[EightPuzzleProblem(initial)], 
       ...:                  searches=[best_first_search, 
       ...:                            iterative_deepening_best_first_search, 
       ...:                            widening_beam_search])
    
