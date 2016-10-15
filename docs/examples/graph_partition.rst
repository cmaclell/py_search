Graph Partition Optimization Example
=====================================

.. ipython::

    In [1]:     from py_search.problems.graph_partition import generate_graph
       ...:     from py_search.problems.graph_partition import random_partition
       ...:     from py_search.problems.graph_partition import LocalGraphPartitionProblem
       ...:     from py_search.problems.graph_partition import cutsize
       ...:     from py_search.optimization import simulated_annealing
       ...:     from py_search.optimization import hill_climbing
       ...:     from py_search.utils import compare_searches
       ...:
       ...:     n = 20
       ...:     p = 10 / (n-1)
       ...:     print(n, p)
       ...:     V, E = generate_graph(n, p)
       ...:     initial = random_partition(V)
       ...:
       ...:     print("######################################")
       ...:     print("Local Search / Optimization Techniques")
       ...:     print("######################################")
       ...:
       ...:     problem = LocalGraphPartitionProblem(initial, extra=(V,E)) 
       ...:     print("Initial Partition Cost:")
       ...:     print(cutsize(E, initial))
       ...:     print()
       ...:
       ...:     def annealing(problem):
       ...:         size = (n * (n//2)) // 2
       ...:         return simulated_annealing(problem, initial_temp=5.5, 
       ...:                                    temp_length=size)
       ...:
       ...:     def greedy_annealing(problem):
       ...:         size = (n * (n//2)) // 2
       ...:         return simulated_annealing(problem, initial_temp=0,
       ...:                                     temp_length=size)
       ...:
       ...:     compare_searches(problems=[problem],
       ...:                      searches=[hill_climbing, annealing, 
       ...:                                greedy_annealing])
