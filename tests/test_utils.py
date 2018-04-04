from py_search.utils import weighted_choice
from py_search.utils import timefun


@timefun
def add_values(m):
    return sum([i for i in range(m)])


def test_weighted_choice():
    options = [(1, 'a'), (1, 'b'), (1, 'c')]
    s = set(weighted_choice(options) for i in range(1000))
    assert s.issubset(set(['a', 'b', 'c']))


def test_timefun():
    add_values(10)
