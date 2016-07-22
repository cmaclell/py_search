N-Queens Search Example
=======================

.. ipython::

    In [1]: from py_search.problems.nqueens import nQueens
       ...: from py_search.problems.nqueens import nQueensProblem
       ...: from py_search.problems.nqueens import LocalnQueensProblem
       ...: from py_search.uninformed import depth_first_search
       ...: from py_search.uninformed import breadth_first_search
       ...: from py_search.informed import best_first_search
       ...: from py_search.informed import beam_search
       ...: from py_search.optimization import simulated_annealing
       ...: from py_search.optimization import hill_climbing
       ...: from py_search.utils import compare_searches
       ...: print("###################")
       ...: print("BACKTRACKING SEARCH")
       ...: print("###################")
       ...: initial = nQueens(5)
       ...: print("Empty %i-Queens Problem" % initial.n)
       ...: print(initial)
       ...: print()
       ...: compare_searches(problems=[nQueensProblem(initial)],
       ...:                  searches=[depth_first_search,
       ...:                            breadth_first_search,
       ...:                            best_first_search,
       ...:                            beam_search])
       ...: print()
       ...: print("##########################")
       ...: print("LOCAL SEARCH / OPTIMZATION")
       ...: print("##########################")
       ...: initial = nQueens(20)
       ...: initial.randomize()
       ...: print("Random %i-Queens Problem" % initial.n)
       ...: print(initial)
       ...: print()
       ...: compare_searches(problems=[LocalnQueensProblem(initial)],
       ...:                  searches=[best_first_search,
       ...:                            beam_search,
       ...:                            hill_climbing,
       ...:                            simulated_annealing])
       ...: print()
       ...: initial = nQueens(50)
       ...: initial.randomize()
       ...: print("Random %i-Queens Problem" % initial.n)
       ...: print(initial)
       ...: print()
       ...: compare_searches(problems=[LocalnQueensProblem(initial)],
       ...:                  searches=[hill_climbing,
       ...:                            simulated_annealing]) 
