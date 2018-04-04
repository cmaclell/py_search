from random import shuffle

from py_search.base import FIFOQueue
from py_search.base import LIFOQueue
from py_search.base import PriorityQueue
from py_search.base import Fringe
from py_search.base import Problem
from py_search.base import AnnotatedProblem
from py_search.base import Node


def test_problem():
    """
    Tests to make sure exceptions are raised.
    """
    p = Problem(None)

    try:
        p.predecessors(p.initial)
        assert False
    except NotImplementedError:
        pass

    try:
        p.successors(p.initial)
        assert False
    except NotImplementedError:
        pass

    try:
        p.random_node()
        assert False
    except NotImplementedError:
        pass

    # test to make sure the goal test falls back on the goal specified during
    # problem construction. In this case None == None - CM
    assert p.goal_test(p.initial)

    ap = AnnotatedProblem(p)

    # Should fall back on problem, which will raise an exception.
    try:
        ap.random_node()
        assert False
    except NotImplementedError:
        pass


def test_fringe():

    f = Fringe()

    try:
        f.push(1)
        assert False
    except NotImplementedError:
        pass

    try:
        f.pop()
        assert False
    except NotImplementedError:
        pass

    try:
        len(f)
        assert False
    except NotImplementedError:
        pass

    try:
        list(f)
        assert False
    except NotImplementedError:
        pass


def test_node():
    node1 = Node(1, node_cost=1)
    node2 = Node(2, node_cost=2)

    assert node1 < node2
    assert node1 != node2

    assert repr(node1) == "Node(%s)" % repr(1)
    assert repr(node1) != repr(node2)


def test_fifo_queue():
    """
    Ensure that elements are added and removed in a first in
    first out order.
    """
    random_elements = [i for i in range(10)]
    shuffle(random_elements)

    fifo = FIFOQueue()
    for e in random_elements:
        fifo.push(e)
    output = []
    while len(fifo) > 0:
        output.append(fifo.pop())

    assert output == random_elements


def test_lifo_queue():
    """
    Ensure that all elements are added and removed in a last in
    first out order.
    """
    random_elements = [i for i in range(10)]
    shuffle(random_elements)

    lifo = LIFOQueue()
    for e in random_elements:
        lifo.push(e)
    output = []
    while len(lifo) > 0:
        output.append(lifo.pop())

    random_elements.reverse()
    assert output == random_elements


def test_priority_queue():
    """
    Ensure the priority set is sorting elements correctly.
    """
    random_elements = [i for i in range(10)]
    shuffle(random_elements)

    pq = PriorityQueue(node_value=lambda x: x)
    for e in random_elements:
        pq.push(e)
    output = []
    while len(pq) > 0:
        output.append(pq.pop())

    random_elements.sort()
    assert output == random_elements


def test_priority_queue_max_length():
    """
    Ensure the priority queue is enforcing a max length
    """
    random_elements = [i for i in range(10)]
    shuffle(random_elements)

    pq = PriorityQueue(node_value=lambda x: x, max_length=3)
    for e in random_elements:
        pq.push(e)
    output = []
    while len(pq) > 0:
        output.append(pq.pop())

    random_elements.sort()
    assert output == random_elements[:3]


def test_priority_queue_cost_limit():
    """
    Ensure the priority queue is enforcing a cost limit
    """
    random_elements = [i for i in range(10)]
    shuffle(random_elements)

    pq = PriorityQueue(node_value=lambda x: x, cost_limit=3)
    for e in random_elements:
        pq.push(e)
    output = []
    while len(pq) > 0:
        output.append(pq.pop())

    random_elements.sort()
    assert output == random_elements[:4]
