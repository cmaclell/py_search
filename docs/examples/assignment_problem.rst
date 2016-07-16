Assignment Problem Optimization Example
========================================

.. ipython::

    In [1]:     from munkres import Munkres
       ...:     from py_search.assignment_problem import random_matrix
       ...:     from py_search.assignment_problem import print_matrix
       ...:     from py_search.assignment_problem import cost
       ...:     from py_search.assignment_problem import random_assignment
       ...:     from py_search.assignment_problem import AssignmentProblem
       ...:     from py_search.assignment_problem import TAssignmentProblem
       ...:     from py_search.search import beam_optimization
       ...:     from py_search.search import simulated_annealing_optimization
       ...:     from py_search.search import hill_climbing_optimization
       ...:     from py_search.search import beam_search
       ...:     from py_search.search import best_first_search
       ...:     from py_search.search import compare_searches
       ...:
       ...:     n = 8
       ...:     costs = random_matrix(n)
       ...: 
       ...:     print("####################################################")
       ...:     print("Optimial solution using Munkres/Hungarian Algorithm")
       ...:     print("####################################################")
       ...: 
       ...:     m = Munkres()
       ...:     indices = m.compute(costs)
       ...:     best = tuple([v[1] for v in indices])
       ...:     print("Munkres Solution:")
       ...:     print(best)
       ...:     print("Munkres Cost:")
       ...:     print(cost(best, costs))
       ...:     print()
       ...: 
       ...:     print("####################################")
       ...:     print("Local Search Optimization Techniques")
       ...:     print("####################################")
       ...: 
       ...:     initial = random_assignment(n)
       ...:     problem = AssignmentProblem(initial, initial_cost=cost(initial, costs),
       ...:                                 extra=(costs,)) 
       ...:     print("Initial Assignment (randomly generated):")
       ...:     print(initial)
       ...:     print("Initial Assignment Cost:")
       ...:     print(problem.initial.cost())
       ...:     print()
       ...: 
       ...: 
       ...:     def beam_width2(problem):
       ...:         return beam_optimization(problem, beam_width=2)
       ...:     def annealing_2000steps(problem):
       ...:         return simulated_annealing_optimization(problem, limit=2000)
       ...: 
       ...:     compare_searches(problems=[problem],
       ...:                      searches=[hill_climbing_optimization ,beam_width2, 
       ...:                                annealing_2000steps])
       ...: 
       ...:     print()
       ...:     print("####################################")
       ...:     print("Tree Search Optimization Techniques")
       ...:     print("####################################")
       ...: 
       ...:     # TREE SEARCH APPROACH
       ...:     empty = tuple([None for i in range(len(costs))])
       ...:     unassigned = [i for i in range(len(costs))]
       ...: 
       ...:     new_costs = [[c - min(row) for c in row] for row in costs]
       ...:     min_c = [min([row[c] for row in costs]) for c,v in enumerate(costs[0])]
       ...:     new_costs = [[v - min_c[c] for c, v in enumerate(row)] for row in costs]
       ...: 
       ...:     tree_problem = TAssignmentProblem(empty, extra=(costs, unassigned)) 
       ...: 
       ...:     def tree_beam_width2(problem):
       ...:         return beam_search(problem, beam_width=2)
       ...: 
       ...:     print()
       ...:     compare_searches(problems=[tree_problem],
       ...:                      searches=[tree_beam_width2,
       ...:                                best_first_search])
       ...: 

