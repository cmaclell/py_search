Assignment Problem Optimization Example
========================================

.. ipython::

    In [1]:     from munkres import Munkres
       ...:     from py_search.problems.assignment_problem import random_matrix
       ...:     from py_search.problems.assignment_problem import print_matrix
       ...:     from py_search.problems.assignment_problem import cost
       ...:     from py_search.problems.assignment_problem import random_assignment
       ...:     from py_search.problems.assignment_problem import LocalAssignmentProblem
       ...:     from py_search.problems.assignment_problem import AssignmentProblem
       ...:     from py_search.optimization import local_beam_search
       ...:     from py_search.optimization import simulated_annealing
       ...:     from py_search.optimization import hill_climbing
       ...:     from py_search.informed import beam_search
       ...:     from py_search.informed import best_first_search
       ...:     from py_search.utils import compare_searches
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
       ...:     print("######################################")
       ...:     print("Local Search / Optimization Techniques")
       ...:     print("######################################")
       ...: 
       ...:     initial = random_assignment(n)
       ...:     problem = LocalAssignmentProblem(initial, initial_cost=cost(initial, costs),
       ...:                                 extra=(costs,)) 
       ...:     print("Initial Assignment (randomly generated):")
       ...:     print(initial)
       ...:     print("Initial Assignment Cost:")
       ...:     print(problem.initial.cost())
       ...:     print()
       ...: 
       ...:     def local_beam_width2(problem):
       ...:         return local_beam_search(problem, beam_width=2)
       ...: 
       ...:     def greedy_annealing(problem):
       ...:         num_neighbors = (n * (n-1)) // 2
       ...:         return simulated_annealing(problem, initial_temp=0,
       ...:                                    temp_length=num_neighbors)
       ...: 
       ...:     def annealing(problem):
       ...:         num_neighbors = (n * (n-1)) // 2
       ...:         return simulated_annealing(problem, initial_temp=1.5,
       ...:                                    temp_length=num_neighbors)
       ...:     compare_searches(problems=[problem],
       ...:                      searches=[hill_climbing, local_beam_width2, 
       ...:                                annealing, greedy_annealing])
       ...: 
       ...:     print()
       ...:     print("###########################")
       ...:     print("Informed Search Techniques")
       ...:     print("###########################")
       ...: 
       ...:     # TREE SEARCH APPROACH
       ...:     empty = tuple([None for i in range(len(costs))])
       ...:     unassigned = [i for i in range(len(costs))]
       ...: 
       ...:     new_costs = [[c - min(row) for c in row] for row in costs]
       ...:     min_c = [min([row[c] for row in costs]) for c,v in enumerate(costs[0])]
       ...:     new_costs = [[v - min_c[c] for c, v in enumerate(row)] for row in costs]
       ...: 
       ...:     tree_problem = AssignmentProblem(empty, extra=(costs, unassigned)) 
       ...: 
       ...:     def beam_width2(problem):
       ...:         return beam_search(problem, beam_width=2)
       ...: 
       ...:     print()
       ...:     compare_searches(problems=[tree_problem],
       ...:                      searches=[beam_width2,
       ...:                                best_first_search])
       ...: 

