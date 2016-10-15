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
       ...:
       ...: def beam2(problem):
       ...:     return local_beam_search(problem, beam_width=2, cost_limit=0)
       ...:
       ...: def steepest_hill(problem):
       ...:     return hill_climbing(problem, cost_limit=0)
       ...:
       ...: def annealing(problem):
       ...:     size = problem.initial.state.n
       ...:     n_neighbors = (size * (size-1)) // 2
       ...:     return simulated_annealing(problem, cost_limit=0,
       ...:                                initial_temp=1.8,
       ...:                                temp_length=n_neighbors)
       ...:
       ...: def greedy_annealing(problem):
       ...:     size = problem.initial.state.n
       ...:     n_neighbors = (size * (size-1)) // 2
       ...:     return simulated_annealing(problem, cost_limit=0,
       ...:                                initial_temp=0,
       ...:                                temp_length=n_neighbors)
       ...:
       ...: compare_searches(problems=[LocalnQueensProblem(initial)],
       ...:                  searches=[best_first_search,
       ...:                            beam2,
       ...:                            steepest_hill,
       ...:                            annealing, greedy_annealing])
       ...: print()
       ...: initial = nQueens(50)
       ...: initial.randomize()
       ...: print("Random %i-Queens Problem" % initial.n)
       ...: print(initial)
       ...: print()
       ...: compare_searches(problems=[LocalnQueensProblem(initial)],
       ...:                  searches=[steepest_hill,
       ...:                            annealing, greedy_annealing]) 
