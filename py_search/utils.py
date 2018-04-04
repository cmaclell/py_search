"""
Utilities for the py_search library.
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from tabulate import tabulate
from random import uniform
from functools import wraps
from functools import partial
import timeit

from py_search.base import AnnotatedProblem


def weighted_choice(choices):
    """
    Given a list of weighted choices, choose one.  Choices are a list of
    (weight, element) pairs.
    """
    total = sum(w for w, c in choices)
    r = uniform(0, total)
    upto = 0
    for w, c in choices:
        if upto + w >= r:
            return c
        upto += w


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
            start_time = timeit.default_timer()

            try:
                sol = next(search(annotated_problem))
                elapsed = timeit.default_timer() - start_time
                cost = sol.cost()
            except StopIteration:
                elapsed = timeit.default_timer() - start_time
                cost = 'Failed'

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


def timefun(f):
    """
    A decorator function for calling Timer with autorange on the provided
    function.
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        result = timeit.Timer(partial(f, *args, **kwds)).autorange()
        a = [a for a in args]
        a += ["%s=%s" % (k, kwds[k]) for k in kwds]
        print("Timing %s%s: %0.7f (num runs=%i)" % (f.__name__, tuple(a),
                                                    result[1], result[0]))
        return f(*args, **kwds)

    return wrapper
