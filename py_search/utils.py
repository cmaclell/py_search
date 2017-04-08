"""
Utilities for the py_search library.
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from tabulate import tabulate
import timeit

from py_search.base import AnnotatedProblem


def compare_searches(problems, searches):
    """
    A function for comparing different search algorithms on different problems.

    :param problems: problems to solve.
    :type problems: an iterator of problems (usually a list)
    :param searches: search algorithms to use.
    :type searches: an iterator of search functions (usually a list)
    """
    table = []

    for problem in problems:
        for search in searches:
            annotated_problem = AnnotatedProblem(problem)

            try:
                start_time = timeit.default_timer()
                sol = next(search(annotated_problem))
                elapsed = timeit.default_timer() - start_time
                cost = sol.cost()
            except StopIteration:
                value = 'Failed'
                elapsed = 'Failed'

            table.append([problem.__class__.__name__, search.__name__,
                          annotated_problem.goal_tests,
                          annotated_problem.nodes_expanded,
                          annotated_problem.nodes_evaluated, "%0.3f" % cost if
                          isinstance(cost, float) else cost,
                          "%0.4f" % elapsed if isinstance(elapsed, float) else
                         elapsed])

    print(tabulate(table, headers=['Problem', 'Search Alg', 'Goal Tests',
                                   'Nodes Expanded', 'Nodes Evaluated',
                                   'Solution Cost', 'Runtime'],
                   tablefmt="simple"))
