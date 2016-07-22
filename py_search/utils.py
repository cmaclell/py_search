"""
Utilities for the py_search library.
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from tabulate import tabulate

from py_search.base import AnnotatedProblem

def compare_searches(problems, searches):
    """
    A function for comparing different search algorithms on different problems.

    :param problems: problems to solve.
    :type problems: typically a list of problems, but could be an iterator
    :param searches: search algorithms to use.
    :type searches: typically a list of search functions, but could be an iterator
    """
    table = []

    for problem in problems:
        for search in searches:
            annotated_problem = AnnotatedProblem(problem)

            try:
                sol = next(search(annotated_problem))
                value = problem.node_value(sol)
            except StopIteration:
                value = 'Failed'

            table.append([problem.__class__.__name__, search.__name__,
                          annotated_problem.goal_tests,
                          annotated_problem.nodes_expanded,
                          annotated_problem.nodes_evaluated, "%0.3f" % value if
                          isinstance(value, float) else value])

    print(tabulate(table, headers=['Problem', 'Search Alg', 'Goal Tests',
                                   'Nodes Expanded', 'Nodes Evaluated',
                                   'Solution Cost'],
                   tablefmt="simple"))
